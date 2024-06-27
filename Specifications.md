
# Introduction:

Our current python scanner supports Python3 versions till version [3.5.5](https://wiki.veracode.local/display/RES/Python+3+API+support). This research spec is to update our python3 support to version 3.7.4. 


# Modeling Details:

## Custom Handlers:
There is provision to create custom loggers by extending one of the handlers provided in [logging.handlers](https://docs.python.org/3.6/library/logging.handlers.html#module-logging.handlers) package. 

If one of the below methods is extended in a custom handler logger class, it should be considered entry points. Its parameter is considered tainted, based on how handler is being called. 

Entry Point methods:

```
T = tainted only if, one of the info, debug, warn,error methods are called on this custom logger with tainted data.

handle(T)
format(T)
emit(T)
```

For e.g. in below case `emit` is entry point, with tainted `record` value, since  its called with logging.debug(T).

```

class TTSHandler(logging.Handler):
        # Entry point, and model if record is tainted
        def emit(self, record):
                print('emit')
                msg = self.format(record)
                cmd = [msg]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
                # wait for the program to finish
                print(p.stdout.readline())
                p.communicate()


def configure_logging():
    h = TTSHandler()
    root = logging.getLogger()
    root.addHandler(h)
    # the default formatter just returns the message
    root.setLevel(logging.DEBUG)

def main(msg):
    # Tainted data is being passed to custom handler
    logging.debug(msg) # CWEID 117

if __name__ == '__main__':
    configure_logging()
    # Taint is being passed
    sys.exit(main(sys.argv[1]))

```


## [PEP 468 Preserving the order of **kwargs in a function](https://www.python.org/dev/peps/pep-0468/): 

Look into usecases, does this impact with our tainted sources order in a function signature.

## String Formatting:

New kind of formatting string literals are introduced [PEP 498](https://www.python.org/dev/peps/pep-0498/)
Also, check if string.format is being modeled so far in our current python 2 & 3 support.

## await/yield/aync:

[PEP 492](https://www.python.org/dev/peps/pep-0492), [PEP 525](https://www.python.org/dev/peps/pep-0525) and [PEP 530](https://www.python.org/dev/peps/pep-0530), think if there are ways to exploit this functionality.

# Taint Analysis:

|Module|Class|Entry Point|SOURCE|Prop|Sink|CWEID|Testcase|Notes|
|---|---|---|---|---|---|---|---|---|
|[secrets](https://docs.python.org/3/library/secrets.html#module-secrets)||||||||Note that the pseudo-random generators in the random module should NOT be used for security purposes. Use secrets on Python 3.6+ and os.urandom() on Python 3.5 and earlier.<BR>[random](https://docs.python.org/3/library/random.html#module-random) module uses Mersenne Twister RNG, which is not suited for cryptographic usages.<BR><BR><BR><BR>Change messages_en-us.txt:<BR>**RANDMSG_python**: <span>Standard random number generators do not provide a sufficient amount of entropy when used for security purposes. Attackers can brute force the output of pseudorandom number generators such as rand().</span> <span>If this random number is used where security is a concern such as generating passwords, session keys, authentication etc; use a trusted cryptographic random number generator instead.  The new secrets module introduced in Python 3.6, is used for generating such cryptographically strong random number genertors. For security sensitive software, its still better to use cryptography.io</span> <span>References: <a href="http://cwe.mitre.org/data/definitions/331.html">CWE</a> <BR> <a href="https://docs.python.org/3/library/secrets.html#module-secrets">secrets module</a><BR><a href="https://cryptography.io/en/latest/">cryptography.io</a></span>
|[asyncio](https://docs.python.org/3/library/asyncio.html#module-asyncio)|||||create_subprocess_shell(T,...)<BR>create_subprocess_exec(T,...)|78||[asyncio details](https://docs.python.org/3/whatsnew/3.6.html#asyncio)<BR>Its all about keeping up with asynchronous processing... If coroutines can be injected as tainted source, would be cool. There are some high level and low level APIs, which needs to be tagged as sinks... Lot more time/thinking needed. Low Level APIs are for library and framework usage only, so not supported.
|[pathlib](https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib)|[Path](https://docs.python.org/3/library/pathlib.html?highlight=pathlib#concrete-paths)||||Path(T)<BR>PosixPath(T)<BR>WindowsPath(T)<BR>T.stat()<BR>T.chmod()<BR>T.exists()<BR>T.expanduser()<BR>T.lchmod()<BR>T.lstat()<BR>T.open()<BR>T.rename(...)<BR>p.rename(T)<BR>T.replace(...)<BR>p.replace(T)<BR>T.rmdir()<BR>T.symlink_to()<BR>T.link_to()<BR>|73||[PEP 519](https://www.python.org/dev/peps/pep-0519/)<BR>pathlib introduced 2 types of paths, pure paths and concrete paths. pure paths is mainly making paths os agnostics, without any OS level operations... concrete paths would be thru which i/o operations on file system s would be happening. Thus, all 73 would be in concrete path hierarchy|
|[concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html#)||||||||Its all about keeping up with asynchronous processing... If coroutines can be injected as tainted source, would be cool. There are some high level and low level APIs, which needs to be tagged as sinks... Lot more time/thinking needed. Low Level API not supported.
|[importlib](https://docs.python.org/3/library/importlib.html)||||||||There doesn't seem to be a way to load anything which isn't on sys.modules/pythonpath already... So, no way to install something unsafe directly from internet. Also, this is a very legit way to import modules/packages dynamically... so could get noisy even if could be hacked.
|[json](https://docs.python.org/3/library/json.html)||||||||json module is not suspectible to deserialization issues. No SINKs to report here.
|[logging.handlers](https://docs.python.org/3/library/logging.handlers.html)||||||||No new sinks, some modeling required to detect custom loggers. Some testcases added to make sure specialized loggers are being handled well. <BR> Not all loggers being used are unsafe against 117 (CRLF Injections), but its going to be a lot more work for scanner to differentiate and than flag. So, if we hear more complaints, we will leave it as it is. Just for record, all specialized loggers (Stream, File, Null) and custom handler based loggers are safe from CRLF Injection. Only one problematic is [log_forging_simple.py](https://gitlab.laputa.veracode.io/research-roadmap/python_refresh_3.5_3.7/blob/master/testcases/logging/log_forging_simple.py)
|[multiprocessing](https://docs.python.org/3/library/multiprocessing.html)||||||||Target needs to be importable... Thus, no way to run any unsafe code without importing.
|[socket](https://docs.python.org/3/library/socket.html)|||||create_connection(insecure,...)<BR>create_server(insecure_addr,...)<BR>bind(insecure_addr)<BR>connect(insecure_addr)<BR>connect_ex(insecure_addr)<BR>sendto(..., insecure_addr)|923||`insecure_addr` will be defined in one of the below ways: <BR> 2-tuple pair (host,port) or <BR>HOST=''<BR>PORT=8080<BR>s.connect(HOST,PORT).<BR>When host value is '', flag as 923
||||T == Tainted:<BR><BR>T = T.recv()<BR>T = T.recvfrom()<BR>T = T.recvmsg()<BR>T.recvmsg_into(tainted_buffer)<BR>T.recvfrom_into(tainted_buffer)<BR>T.recv_into(tainted_buffer)<BR>||create_connection(insecure,...)<BR>create_server(insecure_addr,...)<BR>bind(insecure_addr)<BR>connect(insecure_addr)<BR>connect_ex(insecure_addr)<BR>sendto(..., insecure_addr)|923||`insecure_addr` will be defined in one of the below ways: <BR> 2-tuple pair (host,port) or <BR>HOST=''<BR>PORT=8080<BR>s.connect(HOST,PORT).<BR>When host value is '', flag as 923
||||||insecure_adr == Tainted<BR><BR>T.listen()<BR>create_connection(...,insecure_adr)<BR>create_server(insecure_adr,...)<BR>bind(insecure_adr)<BR>connect(insecure_adr)<BR>connect_ex(insecure_adr)<BR>sendto(...,insecure_adr)<BR>|99
||||||T == Taint.Sensitive<BR><BR>send(T)<BR>sendall(T)<BR>sendto(T)<BR>sendmsg(T)<BR>|201
||||||T = Network.Tainted<BR><BR>sendfile(T)<BR>|73
|[socketserver](https://docs.python.org/3/library/socketserver.html#module-socketserver)|
|[ssl](https://docs.python.org/3/library/ssl.html#module-ssl)||||||||[ssl details](https://docs.python.org/3/whatsnew/3.7.html#ssl)
|[zlib](https://docs.python.org/3.6/library/zlib.html)|
|[http.client](https://docs.python.org/3/library/http.client.html)|[HTTPConnection](https://docs.python.org/3/library/http.client.html#httpconnection-objects)||T == Network.Tainted:<BR>T = getresponse()|||||Not recommended way to make http connection. Also, not used by customers either. So lightly modeling it, to not miss tainted sources just in case.
|[http.client](https://docs.python.org/3/library/http.client.html)|[HTTPResponse](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse)||T == Network.Tainted:<BR>T = read()<BR>readinto(T)<BR>T = getheader()<BR>T = getheaders()<BR>msg<BR>|||||Not recommended way to make http connection. Also, not used by customers either. So lightly modeling it, to not miss tainted sources just in case.
|[http.server](https://docs.python.org/3/library/http.server.html)||||||||This class is not recommended to be used in production. So, lets not specc all handlers. Instead just flag its usage as insecure. ToDo: Find correct CWE to report.
|[zipapp](https://docs.python.org/3.5/library/zipapp.html#module-zipapp)|

# Testcase:

Design Considerations:
- Use [PEP-520](https://www.python.org/dev/peps/pep-0520/), [PEP-468](https://www.python.org/dev/peps/pep-0468/)

# ToDo:
- File management:
	- os.readline()/write(0 etc, traditional ways of reading/writing to a file are not specced.
	- Currently, specced Path.read* is 73, Path.write is also 73, but what should Path.write(tainted_data) be?

# References:

- [Changelog](https://docs.python.org/3/whatsnew/changelog.html)
- [WhatsNew](https://docs.python.org/3/whatsnew/index.html)
- [Current Python 3 Support](https://wiki.veracode.local/display/RES/Python+3+API+support)
- [Python 2 Research Specs](https://wiki.veracode.local/display/RES/Python+Standard+Library)
- [Python 3.0_3.5_Changelog analyzed](https://gitlab.laputa.veracode.io/research-roadmap/python3-api/blob/master/Python3.0-3.5_changes.rst)