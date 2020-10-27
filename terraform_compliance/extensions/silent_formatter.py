# -*- coding: utf-8 -*-

"""
    This radish extension provides the functionality to write the feature file run to the console.
"""

from __future__ import unicode_literals
from __future__ import print_function

import sys
import colorful as cf

from radish.terrain import world
from radish.hookregistry import before, after
from radish.scenariooutline import ScenarioOutline
from radish.scenarioloop import ScenarioLoop
from radish.stepmodel import Step
from radish.extensionregistry import extension
from radish.compat import u

import colorful
from radish.feature import Feature

from radish.utils import console_write as write


@extension
class DotOutputFormatter(object):
    """
    Output formatter in the dot style.
    """

    LOAD_IF = staticmethod(lambda config: config.formatter == "silent_formatter")
    LOAD_PRIORITY = 30


    def __init__(self):
        after.each_feature(self.silent_formatter_after_each_feature)

    def silent_formatter_after_each_feature(self, feature):
        """
            Writes feature header to the console

            :param Feature feature: the feature to write to the console
        """
        if not any(scenario.state == 'failed' for scenario in feature.all_scenarios):
            return

        self.console_writer_before_each_feature(feature)

        for scenario in feature.all_scenarios:
            self.silent_formatter_after_each_scenario(scenario)


    def silent_formatter_after_each_scenario(self, scenario):
        """
            If the scenario is a ExampleScenario it will write the Examples header

            :param Scenario scenario: the scenario which was ran.
        """
        if scenario.state != 'failed':
            return
            # return self.console_writer_after_each_scenario(scenario)

        # self.console_writer_before_each_feature(self.last_feature)

        self.console_writer_before_each_scenario(scenario)

        for step in scenario.all_steps:
            self.console_writer_after_each_step(step)

        for msg in scenario.failed_step.context.failure_msg:
            write(msg)

        return self.console_writer_after_each_scenario(scenario)


    # def dot_formatter_after_each_scenario(self, scenario):
    #     """
    #         If the scenario is a ExampleScenario it will write the Examples header

    #         :param Scenario scenario: the scenario which was ran.
    #     """
    #     if isinstance(scenario, (ScenarioOutline, ScenarioLoop)):
    #         return

    #     sys.stdout.write(u(self.STATE_SYMBOLS[scenario.state]))

    def dot_formatter_after_each_step(self, step):
        if step.state == Step.State.FAILED:
            self._failed_steps.append(step)


    def dot_formatter_failure_summary(self, features, marker):
        """Output summary for failed Scenarios."""
        if not self._failed_steps:
            return

        output = "\n" + cf.bold_white("Failed Scenarios:") + "\n" # could be red

        for step in self._failed_steps:
            output += "{}: {}\n    {}\n".format(
                step.path, step.parent.sentence, cf.red(step.sentence)
            )
            if world.config.with_traceback:
                output += "      {}\n".format(
                    "\n      ".join(
                        [
                            str(cf.red(l))
                            for l in step.failure.traceback.split("\n")[:-2]
                        ]
                    )
                )
            output += "      {}: {}\n\n".format(
                cf.bold_red(step.failure.name), cf.red(step.failure.reason)
            )

        sys.stdout.write(u(output + "\n"))

    # def dot_formatter_failure_summary(self, features, marker):
    #     """Output summary for failed Scenarios."""
    #     if not self._failed_steps:
    #         return

    #     output = "\n" + cf.bold_red("Failures:") + "\n"

    #     for step in self._failed_steps:
    #         output += "{}: {}\n    {}\n".format(
    #             step.path, step.parent.sentence, cf.red(step.sentence)
    #         )
    #         if world.config.with_traceback:
    #             output += "      {}\n".format(
    #                 "\n      ".join(
    #                     [
    #                         str(cf.red(l))
    #                         for l in step.failure.traceback.split("\n")[:-2]
    #                     ]
    #                 )
    #             )
    #         output += "      {}: {}\n\n".format(
    #             cf.bold_red(step.failure.name), cf.red(step.failure.reason)
    #         )

    #     sys.stdout.write(u(output + "\n"))

    def console_writer_after_each_step(self, step):
        """
            Writes the step to the console after it was run

            :param Step step: the step to write to the console
        """
        if not isinstance(step.parent.parent, Feature):
            return

        color_func = self.get_color_func(step.state)
        line_jump_seq = self.get_line_jump_seq() * (
            ((len(step.raw_text) + 3) if step.text else 1)
            + (len(step.table) + 1 if step.table_header else 0)
        )
        output = "{0}        ".format(line_jump_seq)

        if isinstance(step.parent, ScenarioOutline):
            # Highlight ScenarioOutline placeholders e.g. '<method>'
            output += "".join(
                str(
                    colorful.white(item)
                    if (
                        self._placeholder_regex.search(item)
                        and item.strip("<>") in step.parent.examples_header
                    )
                    else color_func(item)
                )
                for item in self._placeholder_regex.split(step.sentence)
            )
        else:
            output += "{0}{1}".format(
                self.get_id_sentence_prefix(step, colorful.bold_cyan),
                color_func(step.sentence),
            )

        if step.text:
            id_padding = self.get_id_padding(len(step.parent.steps))
            output += colorful.bold_white('\n            {0}"""'.format(id_padding))
            output += colorful.cyan(
                "".join(
                    [
                        "\n                {0}{1}".format(id_padding, l)
                        for l in step.raw_text
                    ]
                )
            )
            output += colorful.bold_white('\n            {0}"""'.format(id_padding))

        if step.table_header:
            colored_pipe = colorful.bold_white("|")
            col_widths = self.get_table_col_widths(
                [step.table_header] + step.table_data
            )

            # output table header
            output += "\n          {0} {1} {0}".format(
                colored_pipe,
                (" {0} ")
                .format(colored_pipe)
                .join(
                    str(colorful.white("{1: <{0}}".format(col_widths[i], x)))
                    for i, x in enumerate(step.table_header)
                ),
            )

            # output table data
            for row in step.table_data:
                output += "\n          {0} {1} {0}".format(
                    colored_pipe,
                    (" {0} ")
                    .format(colored_pipe)
                    .join(
                        str(color_func("{1: <{0}}".format(col_widths[i], x)))
                        for i, x in enumerate(row)
                    ),
                )

        write(output)

    def console_writer_after_each_scenario(self, scenario):
        """
            If the scenario is a ExampleScenario it will write the Examples header

            :param Scenario scenario: the scenario which was ran.
        """
        output = ""
        if isinstance(scenario, ScenarioOutline):
            output += "\n    {0}:\n".format(
                colorful.bold_white(scenario.example_keyword)
            )
            output += colorful.bold_white(
                "        {0}| {1} |".format(
                    self.get_id_padding(len(scenario.scenarios), offset=2),
                    " | ".join(
                        "{1: <{0}}".format(scenario.get_column_width(i), x)
                        for i, x in enumerate(scenario.examples_header)
                    ),
                )
            )
        elif isinstance(scenario, ScenarioLoop):
            output += "\n    {0}: {1}".format(
                colorful.bold_white(scenario.iterations_keyword),
                colorful.cyan(scenario.iterations),
            )
        elif isinstance(scenario.parent, ScenarioOutline):
            colored_pipe = colorful.bold_white("|")
            color_func = self.get_color_func(scenario.state)
            output += "{0}        {1}{2} {3} {2}".format(
                self.get_line_jump_seq(),
                self.get_id_sentence_prefix(
                    scenario, colorful.bold_cyan, len(scenario.parent.scenarios)
                ),
                colored_pipe,
                (" {0} ")
                .format(colored_pipe)
                .join(
                    str(
                        color_func(
                            "{1: <{0}}".format(scenario.parent.get_column_width(i), x)
                        )
                    )
                    for i, x in enumerate(scenario.example.data)
                ),
            )

            if scenario.state == Step.State.FAILED:
                failed_step = scenario.failed_step
                if world.config.with_traceback:
                    output += "\n          {0}{1}".format(
                        self.get_id_padding(len(scenario.parent.scenarios)),
                        "\n          ".join(
                            [
                                str(colorful.red(l))
                                for l in failed_step.failure.traceback.split("\n")[:-2]
                            ]
                        ),
                    )
                output += "\n          {0}{1}: {2}".format(
                    self.get_id_padding(len(scenario.parent.scenarios)),
                    colorful.bold_red(failed_step.failure.name),
                    colorful.red(failed_step.failure.reason),
                )
        elif isinstance(scenario.parent, ScenarioLoop):
            colored_pipe = colorful.bold_white("|")
            color_func = self.get_color_func(scenario.state)
            output += "{0}        {1}{2} {3: <18} {2}".format(
                self.get_line_jump_seq(),
                self.get_id_sentence_prefix(
                    scenario, colorful.bold_cyan, len(scenario.parent.scenarios)
                ),
                colored_pipe,
                str(color_func(scenario.iteration)),
            )

            if scenario.state == Step.State.FAILED:
                failed_step = scenario.failed_step
                if world.config.with_traceback:
                    output += "\n          {0}{1}".format(
                        self.get_id_padding(len(scenario.parent.scenarios)),
                        "\n          ".join(
                            [
                                str(colorful.red(l))
                                for l in failed_step.failure.traceback.split("\n")[:-2]
                            ]
                        ),
                    )
                output += "\n          {0}{1}: {2}".format(
                    self.get_id_padding(len(scenario.parent.scenarios)),
                    colorful.bold_red(failed_step.failure.name),
                    colorful.red(failed_step.failure.reason),
                )

        if output:
            write(output)
    
    def get_color_func(self, state):
        """
            Returns the color func to use
        """
        if state == Step.State.PASSED:
            return colorful.bold_green
        elif state == Step.State.FAILED:
            return colorful.bold_red
        elif state == Step.State.PENDING:
            return colorful.bold_yellow
        elif state:
            return colorful.cyan

    def get_line_jump_seq(self):
        """
            Returns the line jump ANSI sequence
        """
        line_jump_seq = ""
        if (
            not world.config.no_ansi
            and not world.config.no_line_jump
            and not world.config.write_steps_once
        ):
            line_jump_seq = "\r\033[A\033[K"
        return line_jump_seq

    def get_id_sentence_prefix(self, model, color_func, max_rows=None):
        """
            Returns the id from a model as sentence prefix

            :param Model model: a model with an id property
            :param function color_func: a function which gives coloring
            :param int max_rows: the maximum rows. Used for padding
        """
        padding = len("{0}. ".format(max_rows)) if max_rows else 0
        return (
            color_func("{1: >{0}}. ".format(padding, model.id))
            if world.config.write_ids
            else ""
        )

    def get_id_padding(self, max_rows, offset=0):
        """
            Returns the id padding
        """
        if not world.config.write_ids:
            return ""

        return " " * (len(str(max_rows)) + 2 + offset)

    def get_table_col_widths(self, table):
        """
            Returns the width for every column of a table (lists in list)
        """
        return [
            max(len(str(col)) for col in row) for row in zip(*table)
        ]  # pylint: disable=star-args



    def console_writer_before_each_scenario(self, scenario):
        """
            Writes the scenario header to the console

            :param Scenario scenario: the scenario to write to the console
        """
        output = "\n"
        if isinstance(scenario.parent, ScenarioOutline):
            if world.config.write_steps_once:
                return

            id_prefix = self.get_id_sentence_prefix(
                scenario, colorful.bold_yellow, len(scenario.parent.scenarios)
            )
            colored_pipe = colorful.bold_white("|")
            output = "        {0}{1} {2} {1}".format(
                id_prefix,
                colored_pipe,
                (" {0} ")
                .format(colored_pipe)
                .join(
                    str(
                        colorful.bold_yellow(
                            "{1: <{0}}".format(scenario.parent.get_column_width(i), x)
                        )
                    )
                    for i, x in enumerate(scenario.example.data)
                ),
            )
        elif isinstance(scenario.parent, ScenarioLoop):
            if world.config.write_steps_once:
                return

            id_prefix = self.get_id_sentence_prefix(
                scenario, colorful.bold_yellow, len(scenario.parent.scenarios)
            )
            colored_pipe = colorful.bold_white("|")
            output = "        {0}{1} {2: <18} {1}".format(
                id_prefix, colored_pipe, str(colorful.bold_yellow(scenario.iteration))
            )
        else:
            id_prefix = self.get_id_sentence_prefix(scenario, colorful.bold_cyan)
            for tag in scenario.tags:
                if (
                    tag.name == "precondition"
                    and world.config.expand
                    and world.config.show
                ):  # exceptional for show command when scenario steps expand and tag is a precondition -> comment it out
                    output += colorful.white(
                        "    # @{0}{1}\n".format(
                            tag.name, "({0})".format(tag.arg) if tag.arg else ""
                        )
                    )
                else:
                    output += colorful.cyan(
                        "    @{0}{1}\n".format(
                            tag.name, "({0})".format(tag.arg) if tag.arg else ""
                        )
                    )
            output += "    {0}{1}: {2}".format(
                id_prefix,
                colorful.bold_white(scenario.keyword),
                colorful.bold_white(scenario.sentence),
            )
        write(output)


    def console_writer_before_each_feature(self, feature):
        """
            Writes feature header to the console

            :param Feature feature: the feature to write to the console
        """
        output = ""
        for tag in feature.tags:
            output += colorful.cyan(
                "@{0}{1}\n".format(tag.name, "({0})".format(tag.arg) if tag.arg else "")
            )

        leading = "\n    " if feature.description else ""

        output += "{0}{1}: {2}  # {3}{4}{5}".format(
            self.get_id_sentence_prefix(feature, colorful.bold_cyan),
            colorful.bold_white(feature.keyword),
            colorful.bold_white(feature.sentence),
            colorful.bold_black(feature.path),
            leading,
            colorful.white("\n    ".join(feature.description)),
        )

        if feature.background:
            output += "\n\n    {0}: {1}".format(
                colorful.bold_white(feature.background.keyword),
                colorful.bold_white(feature.background.sentence),
            )
            for step in feature.background.all_steps:
                output += "\n" + self._get_step_before_output(step, colorful.cyan)

        write(output)
