import smtplib
import sys
from email.mime.text import MIMEText


def parlayx():
    me = '079824'
    you = '525591955015@test-simple.sms.dada.net'
    msg = MIMEText('This is a test message')

    msg['Subject'] = 'Fake Mail'
    msg['From'] = me
    msg['To'] = you
    msg.add_header('Message-ID', '123456567@test-simple.sms.dada.net')
    msg.add_header('X-Dada-MMS-GW-Servicecode', 'test35999')
    msg.add_header('X-Dada-MMS-GW-Phone_company', '55')
    msg.add_header('Received', '(Authenticated sender: test)')

    s = smtplib.LMTP('bacco-pre.dadanoc.com', 35309)
    s.set_debuglevel(1)
    s.sendmail(me, [you], msg.as_string())
    s.quit()

def purebros(identifier=None):
    me = '48XXX'
    you = '+3921234567@purebros.it.mt.sms.dada.net'
    msg = MIMEText('''1st Line!
Second Line!


SPACE!''')

    msg['Subject'] = 'Fake Mail'
    msg['From'] = me
    msg['To'] = you
    msg.add_header('Message-ID', '123456567')
    msg.add_header('X-Dada-MMS-GW-Servicecode', '')
    msg.add_header('X-Dada-MMS-GW-Phone_company', '171')
    msg.add_header('Received', '(Authenticated sender: test)')

    s = smtplib.LMTP('bacco-pre.dadanoc.com', 35309)
    s.set_debuglevel(1)
    s.sendmail(me, [you], msg.as_string())
    s.quit()

def notify(identifier=None):
    me = 'andrea.demarco@dada.net'
    you = '112234@s2s.dada.net'
    msg = MIMEText('S2S')

    msg['Subject'] = 'Fake Mail'
    msg['From'] = me
    msg['To'] = you
    msg.add_header('Message-ID', '123456567')
    msg.add_header('X-Dada-S2s-Remote-Httpurl', '/test_s2s.php')
    msg.add_header('X-Dada-S2s-Remote-Httphost', 'www.tobiacaneschi.com')
    msg.add_header('X-Dada-S2s-Remote-Httpmethod', 'GET')
    msg.add_header('X-Dada-S2s-Remote-Httpheaders', 'User-Agent=Pippo&aaa=dasdas')
    msg.add_header('X-Dada-S2s-Remote-Host', 'www.tobiacaneschi.com')
    msg.add_header('X-Dada-S2s-Remote-Port', '81')
    msg.add_header('X-Dada-S2s-Remote-Httpquery', 'click_id=4446&dada=343&mailto=' + me)

    #s = smtplib.LMTP('xentoodev02.ced', 35409)
    s = smtplib.LMTP('localhost', 35409)
    s.sendmail(me, [you], msg.as_string())
    s.quit()

def openmarket(identifier=''):

    headers = {
        'Message-ID' : '123456567',
        'X-Dada-MMS-GW-Servicecode' : 'openmarkettestfree',
        'X-Dada-MMS-GW-Phone_company' : '25',
        'content-type'                : 'text/plain',
        }

    params = {
        'shortcode' : '10958',
        'msisdn'    : '+13182621021',
        'domain'    : 'openmarket.us.sms.dada.net',
        'port'      : 2025,
        'headers'   : headers,
        'authenticated_sender' : 'test',
        }

    common(params, identifier)

def common(params, identifier):
    msg = MIMEText('Text content - {0}'.format(identifier))

    print 'sending from {s} to {m}'.format(s=params['shortcode'], m=params['msisdn'])
    From = params['shortcode']+'@'+params['domain']
    To   = params['msisdn']   +'@'+params['domain']

    msg['From']    = From
    msg['To']      = To
    msg['Subject'] = 'Subject - {0}'.format(identifier)

    params['headers']['Received'] = \
        '(Authenticated sender: {0})'.format(params['authenticated_sender'])

    for k,v in params['headers'].iteritems():
        msg.add_header(k, v)

    s = smtplib.LMTP('127.0.0.1', params['port'])
    s.sendmail(From,
               [To],
               msg.as_string())
    s.quit()

if __name__ == '__main__':
    #notify()
    openmarket(' '.join(sys.argv))
    #purebros()
