import sys
from time import sleep
from wolf_pack import main
mode = 'dep'
if sys.argv and len(sys.argv) > 1:
    mode = sys.argv[1]
    if mode != '--dev':
        mode = 'dep'
    else:
        mode = 'dev'
main(mode)
while True and mode != 'dev':
    sleep(70)
    main(mode)
