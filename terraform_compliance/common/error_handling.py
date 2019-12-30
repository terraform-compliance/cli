from terraform_compliance.common.exceptions import Failure
from radish import world
from radish.utils import console_write, Failure as RadishFailure, traceback
from radish.stepmodel import Step
import colorful
from mock import patch
from ast import literal_eval


class WrapperError(Exception):
    def __init__(self, exception):
        self.exception = exception
        self.reason = str(exception)
        self.traceback = None
        self.name = exception.__class__.__name__
        self.filename = None
        self.line = 0


# This class only works with steps
class Error(Exception):
    def __init__(self, step_obj, message, exception=Failure):
        self.message = message.split("\n")
        self.exit_on_failure = literal_eval(world.config.user_data['exit_on_failure'])
        self.exception = exception
        self.exception_name = exception.__name__
        self.step_obj = step_obj

        self._process()


    def _process(self):
        # Prepare message
        msg = []
        for msg_index in range(0,len(self.message)):
            if self.exit_on_failure is False:
                msg_header = '{}{}'.format(self.exception_name,
                                           colorful.bold_white(':')) if msg_index == 0 else ' '*(len(self.exception_name)+1)
                msg.append('\t\t\t{} {}'.format(colorful.bold_red(msg_header), colorful.red(self.message[msg_index])))
            else:
                msg.append(self.message[msg_index] if msg_index == 0
                                                   else '{}{} {} {}'.format("\t"*2,
                                                                            ' '*(len(self.exception_name)+1),
                                                                            colorful.bold_white(':'),
                                                                            self.message[msg_index]))

        if self.exit_on_failure is False:
            for message in msg:
                console_write(message)

            self._fail_step(self.step_obj.id, message)
            return

        raise self.exception('\n'.join(msg))

    @patch.object(traceback, 'extract_tb', return_value=None)
    def _fail_step(self, step_id, message, *args):
        for step in self.step_obj.parent.all_steps:
            if step.id == step_id:
                step.state = Step.State.FAILED
                step.failure = WrapperError(self.exception('\r{}'.format(' '*len(self.exception_name))))
