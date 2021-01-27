# netstakt
netstat for Windows without the unfortunate newline when using the -b flag.

netstakt runs the command `> netstat -naob` and returns the output in a columnar format. The advantage of using this over vanilla Windows netstat is the command is included on the same line as the rest of the output, making it simple to parse with findstr. 

## Usage
.\netstakt.py