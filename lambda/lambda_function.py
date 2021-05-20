# -*- coding: utf-8 -*-
# Skill para Alexa para um jogo da forca.
# Para jogo com voz apenas

import random
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from lista_palavras import lista_palavras_forca

allWords = lista_palavras_forca

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler para iniciar a Skill."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        sessionAttributes = handler_input.attributes_manager.session_attributes
        sessionAttributes["palavraEscolhida"] = None
        sessionAttributes["letrasDescobertas"] = []
        sessionAttributes["localizacaoAchadas"] = []
        sessionAttributes["gamePlayingStatus"] = False
        sessionAttributes["tentativasRealizadas"] = []
        speak_output = "Bem vindo ao jogo da forca. Diga 'Vamos jogar' para iniciar o jogo, ou se deseja saber as regras diga 'Como jogar'."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class GamePlayIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GamePlayIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        sessionAttributes = handler_input.attributes_manager.session_attributes
        sessionAttributes["gamePlayingStatus"] = True
        sessionAttributes["palavraEscolhida"] = random.choice(allWords).upper()

        speak_output = "A palavra tem " + str(len(sessionAttributes["palavraEscolhida"])) + " letras."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class IdentificarLetraIntentHandler(AbstractRequestHandler):
    """Handler para identificação da letra."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("IdentificarLetraIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        sessionAttributes = handler_input.attributes_manager.session_attributes
        LetraFaladaValue = ask_utils.request_util.get_slot(handler_input, "LetraFalada").value

        if LetraFaladaValue is not None:
            LetraFaladaValue = LetraFaladaValue[0]
        else:
            speak_output = "Desculpe, não consegui entender, pode repetir?"

        if sessionAttributes["gamePlayingStatus"]:
            if LetraFaladaValue not in sessionAttributes["letrasDescobertas"]:
                if LetraFaladaValue in sessionAttributes["palavraEscolhida"]:
                    localizacaoAchadas = []

                    LocalizacaoVaue = 1
                    for character in sessionAttributes["palavraEscolhida"]:
                        if character == LetraFaladaValue:
                            localizacaoAchadas.append(LocalizacaoVaue)
                            sessionAttributes["localizacaoAchadas"].append(LocalizacaoVaue)
                            sessionAttributes["letrasDescobertas"].append(LetraFaladaValue)
                        LocalizacaoVaue += 1

                    if (len(sessionAttributes["localizacaoAchadas"]) == len(sessionAttributes["palavraEscolhida"])):
                        speak_output = "Você adivinhou com sucesso a palavra " + sessionAttributes[
                            "palavraEscolhida"] + ". Diga 'Vamos Jogar' para iniciar novamente."
                        sessionAttributes["gamePlayingStatus"] = False
                    else:
                        speak_output = "A letra " + LetraFaladaValue + " está presente na palavra nas posições - " + str(
                            localizacaoAchadas) + "."
                else:
                    speak_output = "A letra " + LetraFaladaValue + " não está presente na palavra."
            else:
                speak_output = "A letra " + LetraFaladaValue + " já foi falada."
        else:
            speak_output = "Desculpe, não consegui entender, pode repetir?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Até Logo!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, não conseegui entender, poderia tentar denovo?."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
"""sb.add_request_handler(HelloWorldIntentHandler())"""

# Handlers para adicionar as Intents personalizadas
sb.add_request_handler(GamePlayIntentHandler())
sb.add_request_handler(IdentificarLetraIntentHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
