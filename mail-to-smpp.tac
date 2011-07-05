#!/usr/bin/twistd -noy

import os
from zope.interface import implements

from twisted.application import service, internet
from twisted.internet import protocol, defer

application = service.Application("SMTP Server Tutorial")

######################################################################

from smpp.pdu.operations import *
from smpp.pdu.pdu_types import *
from smpp.twisted.config import SMPPClientConfig
from smpp.twisted.client import SMPPClientFactory, SMPPClientTransceiver, SMPPClientService

import logging

logging.basicConfig(format='%(name)-15s %(message)s')

config = SMPPClientConfig(host='localhost', port=8007, username='uname', password='pwd')
msghandler = lambda _: None
client = SMPPClientTransceiver(config, msghandler)
smpp_client_service = SMPPClientService(client)
smpp_client_service.setServiceParent(application)

######################################################################

def send_mt(headers={}):
    print headers
    pdu = SubmitSM(9284,
        service_type='',
        source_addr_ton=AddrTon.ALPHANUMERIC,
        source_addr_npi=AddrNpi.UNKNOWN,
        source_addr='mobileway',
        dest_addr_ton=AddrTon.INTERNATIONAL,
        dest_addr_npi=AddrNpi.ISDN,
        destination_addr=headers['To'],
        esm_class=EsmClass(EsmClassMode.DEFAULT, EsmClassType.DEFAULT),
        protocol_id=0,
        priority_flag=PriorityFlag.LEVEL_0,
        registered_delivery=RegisteredDelivery(RegisteredDeliveryReceipt.SMSC_DELIVERY_RECEIPT_REQUESTED),
        replace_if_present_flag=ReplaceIfPresentFlag.DO_NOT_REPLACE,
        data_coding=DataCoding(DataCodingScheme.GSM_MESSAGE_CLASS, DataCodingGsmMsg(DataCodingGsmMsgCoding.DEFAULT_ALPHABET, DataCodingGsmMsgClass.CLASS_2)),
        short_message='HELLO',
    )
    return smpp_client_service.client.smpp.sendDataRequest(pdu)ck(

######################################################################

from twisted.mail import smtp

class MessageProcessor(object):
    implements(smtp.IMessage)

    def __init__(self):
        self.headers = {}
        self.data    = []
        self.data_mode = False

    def lineReceived(self, line):
        if line and not self.data_mode:
            k, v = line.split(':', 1)
            self.headers[k] = v.lstrip(' ')
        else:
            if self.data_mode:
                self.data.append(line)
            else:
                self.data_mode = True

    def eomReceived(self):
        self.headers['DATA'] = '\n'.join(self.data)
        return send_mt(self.headers).addCallback(self.responseReceived)

    def connectionLost(self):
        pass

    def responseReceived(self, data):
        print data
        return defer.fail(None)

class MTDelivery(object):
    implements(smtp.IMessageDelivery)

    def validateTo(self, user):
        return lambda: MessageProcessor()

    def validateFrom(self, helo, origin):
        return origin

    def receivedHeader(self, helo, origin, recipients):
        pass

class MailFactory(protocol.ServerFactory):
    protocol = smtp.ESMTP

    def buildProtocol(self, addr):
        p = self.protocol()
        p.delivery = MTDelivery()
        p.factory = self
        return p

smtpServerService = internet.TCPServer(2025, MailFactory())
smtpServerService.setServiceParent(application)

