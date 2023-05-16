from time import sleep
from wolf_pack import main
mode = 'dev'
main(mode)
while True and mode != 'dev':
    sleep(70)
    main(mode)