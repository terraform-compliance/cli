from terraform_compliance.common.exceptions import Failure
from radish import world
from radish.utils import console_write
from terraform_compliance.main import Step
import colorful
from ast import literal_eval
from mock import MagicMock
import os


class WrapperError(Exception):
    def __init__(self, exception):
        self.exception = exception
        self.reason = str(exception)
        self.traceback = "No Traceback"
        self.name = exception.__class__.__name__
        self.filename = None
        self.line = 0


# This class only works with steps
class Error(Exception):
    def __init__(self, step_obj, message, exception=Failure):
        self.message = message.split("\n")
        if isinstance(world.config.user_data['exit_on_failure'], bool):
            self.exit_on_failure = world.config.user_data['exit_on_failure']
            self.no_failure = world.config.user_data['no_failure']
        elif isinstance(world.config.user_data, MagicMock):
            self.exit_on_failure = True
            self.no_failure = False
        else:
            self.exit_on_failure = literal_eval(world.config.user_data['exit_on_failure'])
            self.no_failure = literal_eval(world.config.user_data['no_failure'])
        _TFC_ERROR = os.environ.get('TFC_ERROR')

        if step_obj.context.no_failure:
            self.exception = type(step_obj.context.failure_class, (Exception, ), {})
            self.exception_name = step_obj.context.failure_class
            self.no_failure = True
        elif _TFC_ERROR is None:
            self.exception = exception
            self.exception_name = exception.__name__
        else:
            self.exception = type(_TFC_ERROR, (Exception, ), {})
            self.exception_name = _TFC_ERROR

        self.step_obj = step_obj
        self._process()

    def _process(self):
        # Prepare message
        msg = []
        for msg_index in range(0,len(self.message)):
            if self.exit_on_failure is False or self.no_failure is True:
                msg_header = '{}{}'.format(self.exception_name,
                                           colorful.bold_white(':')) if msg_index == 0 else ' '*(len(self.exception_name)+1)
                if str(world.config.formatter) in ('gherkin'):
                    # this line could be improved by letting radish handle the printing
                    msg.append('\t\t{} {}'.format(colorful.bold_red(msg_header), colorful.red(self.message[msg_index])))
                elif str(world.config.formatter) in ('silent_formatter'):
                    msg.append('{} '.format(colorful.bold_red(msg_header)))
                    msg.append('{}'.format(colorful.red(self.message[msg_index])))

            else:
                msg.append(self.message[msg_index] if msg_index == 0
                                                   else '{}{} {} {}'.format("\t"*2,
                                                                            ' '*(len(self.exception_name)+1),
                                                                            colorful.bold_white(':'),
                                                                            self.message[msg_index]))

        if self.exit_on_failure is False or (self.no_failure is True and msg):

            if str(world.config.formatter) in ('gherkin'):
                for message in msg:
                    console_write(message)
            elif str(world.config.formatter) in ('silent_formatter'):
                if not hasattr(self.step_obj.context, 'failure_msg'): # where to put this
                    self.step_obj.context.failure_msg = []
                self.step_obj.context.failure_msg.extend(msg)


            if self.no_failure is False:
                self._fail_step(self.step_obj.id)
            else:
                self.step_obj.state = Step.State.SKIPPED
                for step in self.step_obj.parent.all_steps:
                    step.runable = False
            return

        if self.no_failure is False:
            raise self.exception('\n'.join(msg))

    def _fail_step(self, step_id):
        for step in self.step_obj.parent.all_steps:
            if step.id == step_id:
                step.state = Step.State.FAILED
                step.failure = WrapperError(self.exception('\r{}'.format(' '*len(self.exception_name))))

        if self.message:
            self.step_obj.failure.traceback = '{}: {}'.format(self.exception_name, '\n'.join(self.message)).replace('\x00', '\\x00').replace('\x08', '\\x08')
