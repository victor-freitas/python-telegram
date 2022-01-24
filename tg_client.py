from django.shortcuts import redirect
from telegram.client import Telegram, AuthorizationState
from telegram.utils import AsyncResult
import logging
from typing import  Optional, Dict, Callable

logger = logging.getLogger()


class TelegramClient(Telegram):
    
    def get_authorization_state(self) -> AsyncResult:
        logger.debug('Getting authorization state')
        data = {'@type': 'getAuthorizationState'}

        return self._send_data(data, result_id='getAuthorizationState')

    def _wait_authorization_result(self, result: AsyncResult) -> AuthorizationState:
        authorization_state = None

        if result:
            result.wait(raise_exc=True)

            if result.update is None:
                raise RuntimeError('Something wrong, the result update is None')

            if result.id == 'getAuthorizationState':
                authorization_state = result.update['@type']
            else:
                authorization_state = result.update['authorization_state']['@type']

        return AuthorizationState(authorization_state)
        

    def _send_phone_number_or_bot_token(self) -> AsyncResult:
        """Sends phone number or a bot_token"""
        if self.phone:
            return self._send_phone_number()

        else:
            raise RuntimeError('Unknown mode: both bot_token and phone are None')

    def _send_phone_number(self) -> AsyncResult:
        logger.info('Sending phone number')
        data = {
            '@type': 'setAuthenticationPhoneNumber',
            'phone_number': self.phone,
            'allow_flash_call': False,
            'is_current_phone_number': True,
        }

        return self._send_data(data, result_id='updateAuthorizationState')       

    def _send_telegram_code(self, code: Optional[str] = None) -> AsyncResult:
        logger.info('Sending code') 
        data = {'@type': 'checkAuthenticationCode', 'code': str(code)}

        return self._send_data(data, result_id='updateAuthorizationState')

    def send_code(self, code: str) -> AuthorizationState:
        result = self._send_telegram_code(self.code)
        self.authorization_state = self._wait_authorization_result(result)

        return self.authorization_state
               