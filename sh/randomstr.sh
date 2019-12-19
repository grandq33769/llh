LC_ALL=C tr -dc ${1:-A-Za-z0-9} < /dev/urandom | fold -w ${2:-32} | head -n 1
