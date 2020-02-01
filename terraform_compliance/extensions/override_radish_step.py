# -*- coding: utf-8 -*-

"""
    This module provides a class to represent a Step
"""

from __future__ import unicode_literals

import base64
import re

from radish.model import Model
from radish.exceptions import RadishError
from radish.terrain import world
from radish.stepregistry import StepRegistry
from radish.matcher import merge_step
from radish import utils


class Step(Model):
    """
        Represents a step
    """

    class State(object):
        """
            Represents the step state

            FIXME: for the python3 version this should be an Enum
        """

        UNTESTED = "untested"
        SKIPPED = "skipped"
        PASSED = "passed"
        FAILED = "failed"
        PENDING = "pending"

    def __init__(self, id, sentence, path, line, parent, runable, context_class=None):
        super(Step, self).__init__(id, None, sentence, path, line, parent)
        self.context_class = context_class
        self.table_header = None
        self.table_data = []
        self.table = []
        self.raw_text = []
        self.definition_func = None
        self.argument_match = None
        self.state = Step.State.UNTESTED
        self.failure = None
        self.runable = runable
        self.as_precondition = None
        self.as_background = None
        self.embeddings = []

    @property
    def context(self):
        """
            Returns the scenario context belonging to this step
        """
        return self.parent.context

    @property
    def expanded_sentence(self):
        """
            Returns the expanded sentence of this step

                * Expand constants
        """
        sentence = self.sentence
        for name, value in self.parent.constants:
            sentence = sentence.replace("${{{0}}}".format(name), value)
        return sentence

    @property
    def context_sensitive_sentence(self):
        """
        Return the context class sensitive
        step sentence.
        """
        sentence = self.expanded_sentence
        if self.context_class:
            return utils.str_lreplace(
                "and ",
                self.context_class.capitalize() + " ",
                sentence,
                flags=re.IGNORECASE,
                )

        return sentence

    @property
    def text(self):
        """
            Returns the additional text of this step as string
        """
        return "\n".join(self.raw_text)

    def _validate(self):
        """
            Checks if the step is valid to run or not
        """

        if not self.definition_func or not callable(self.definition_func):
            raise RadishError(
                "The step '{0}' does not have a step definition".format(self.sentence)
            )

    def run(self):
        """
            Runs the step.
        """
        if not self.runable:
            self.state = Step.State.UNTESTED
            return self.state

        self._validate()
        args, kwargs = self.argument_match.evaluate()

        try:
            if kwargs:
                self.definition_func(self, **kwargs)  # pylint: disable=not-callable
            else:
                self.definition_func(self, *args)  # pylint: disable=not-callable
        except Exception as e:  # pylint: disable=broad-except
            self.state = Step.State.FAILED
            self.failure = utils.Failure(e)
        else:
            if self.state is Step.State.SKIPPED:
                self.skip()
            elif self.failure is not None and self.state is Step.State.FAILED:
                self.state = Step.State.FAILED
            elif self.state is not Step.State.PENDING:
                self.state = Step.State.PASSED
        return self.state

    def debug(self):
        """
            Debugs the step
        """
        if not self.runable:
            self.state = Step.State.UNTESTED
            return self.state

        self._validate()
        args, kwargs = self.argument_match.evaluate()

        pdb = utils.get_debugger()

        try:
            pdb.runcall(self.definition_func, self, *args, **kwargs)
        except Exception as e:  # pylint: disable=broad-except
            self.state = Step.State.FAILED
            self.failure = utils.Failure(e)
        else:
            if self.state is Step.State.SKIPPED:
                self.skip()
            elif self.state is not Step.State.PENDING:
                self.state = Step.State.PASSED
        return self.state

    def skip(self):
        """
            Skips the step
        """
        self.state = Step.State.SKIPPED

    def pending(self):
        """
            Mark the step as pending

            The end report will remind
            about all pending steps.
        """
        self.state = Step.State.PENDING

    def behave_like(self, sentence):
        """
            Make step behave like another one

            :param string sentence: the sentence of the step to behave like
        """
        # check if this step has already failed from a previous behave_like call
        if self.state is Step.State.FAILED:
            return

        # create step according to given sentence
        new_step = Step(None, sentence, self.path, self.line, self.parent, True)
        merge_step(new_step, StepRegistry().steps)

        # run or debug step
        if world.config.debug_steps:
            new_step.debug()
        else:
            new_step.run()

        # re-raise exception if the failed
        if new_step.state is Step.State.FAILED:
            new_step.failure.exception.args = (
                "Step '{0}' failed: '{1}'".format(
                    sentence, new_step.failure.exception.message
                ),
            )
            raise new_step.failure.exception

    def embed(self, data, mime_type="text/plain", encode_data_to_base64=True):
        """
            embed data into step
                - step embedded data can be used for cucumber json reports
                - allow to attach text, html or images

        :param data: data attached to report
            data needs to be encoded in base64 for proper handling by tests reporting tools
            if not encoded in base64 encoded_data_to_base64 needs to be True (default value)
        :param mime_type: image/png, image/bmp, text/plain, text/html
            - mime types with special support by Cucumber reporting
            - other mime types will be handled with default handling
        :param encode_data_to_base64: encode data to base64 if True
        """
        if encode_data_to_base64:
            data = base64.standard_b64encode(data.encode()).decode()
        self.embeddings.append({"data": data, "mime_type": mime_type})
