import colorful

from radish.hookregistry import after
from radish.extensionregistry import extension
from radish.utils import console_write

from radish.extensions.formatters.gherkin import ConsoleWriter
ConsoleWriter.OPTIONS = []

@extension
class SilentFormatter(ConsoleWriter):
    """
        This class is a simple extension to ConsoleWriter (a.k.a config.formatter == 'gherkin')
    """

    LOAD_IF = staticmethod(lambda config: config.formatter == "silent_formatter")
    LOAD_PRIORITY = 30


    def __init__(self):
        after.each_feature(self.silent_formatter_after_each_feature)

    def silent_formatter_after_each_feature(self, feature):
        """
            Writes failing features to the console

            :param Feature feature: the feature to write to the console
        """
        if not any(scenario.state == 'failed' for scenario in feature.all_scenarios):
            return

        # ConsoleWriter.console_writer_before_each_feature(self, feature)
        self.console_writer_before_each_feature(feature)

        for scenario in feature.all_scenarios:
            self.silent_formatter_after_each_scenario(scenario)
        
        # one newline between final scenario and results summary
        console_write('')


    def silent_formatter_after_each_scenario(self, scenario):
        """
            similar to call gherkin's formatter but with appropriate modifications

            :param Scenario scenario: the scenario which was ran.
        """
        if scenario.state != 'failed':
            return

        ConsoleWriter.console_writer_before_each_scenario(self, scenario)

        msg_header = '\t\t\x1b[1m\x1b[31mFailure\x1b[1m\x1b[37m:\x1b[22m\x1b[39m\x1b[1m\x1b[31m\x1b[22m\x1b[39m\x1b[26m \x1b[31m'
        for step in scenario.all_steps:
            if step.state == step.State.FAILED:
                # hardcoded formatting
                if len(step.context.failure_msg) == 2:
                    step.failure.reason = step.context.failure_msg[1]

                elif len(step.context.failure_msg) > 2:
                    out = '{}\n\t  '.format(step.context.failure_msg[1]) # radish fills the header for the first message
                    messages = step.context.failure_msg[3::2] # remaining messages
                    headers = step.context.failure_msg[2::2] # remaining headers headers
                    out += '\n\t  '.join(['{} {}'.format(headers[i], messages[i]) for i in range(len(messages))])
                    step.failure.reason = out

            self.console_writer_after_each_step(step)

        self.console_writer_after_each_scenario(scenario)

