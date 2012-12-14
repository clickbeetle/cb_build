#!/bin/bash
# create minimal set of device nodes
install -d ${ROOT}/{proc,sys,dev/pts,dev/shm}

mknod() {
        echo "Creating device node $1"
        /bin/mknod $* || return 1
}

cd ${ROOT}/dev || die "Could not change directory to $2."

! [ -c console ] && rm -rf console
[ -e console ] || { mknod console c 5 1 && chmod 600 console; } || die

! [ -c null ] && rm -rf null
[ -e null ] || { mknod null c 1 3 && chmod 777 null; } || die

! [ -c tty ] && rm -rf tty
[ -e tty ] || { mknod tty c 5 0 && chmod 666 tty; } || die

! [ -c ttyp0 ] && rm -rf ttyp0
[ -e ttyp0 ] || { mknod ttyp0 c 3 0 && chmod 644 ttyp0; } || die

! [ -c ptyp0 ] && rm -rf ptyp0
[ -e ptyp0 ] || { mknod ptyp0 c 2 0 && chmod 644 ptyp0; } || die

! [ -c ptmx ] && rm -rf ptmx
[ -e ptmx ] || { mknod ptmx c 5 2 && chmod 666 ptmx; } || die

! [ -c urandom ] && rm -rf urandom
[ -e urandom ] || { mknod urandom c 1 9 && chmod 666 urandom; } || die

! [ -c random ] && rm -rf random
[ -e random ] || { mknod random c 1 8 && chmod 666 random; } || die

! [ -c zero ] && rm -rf zero
[ -e zero ] || { mknod zero c 1 5 && chmod 666 zero; } || die

! [ -c kmsg ] && rm -rf kmsg
[ -e kmsg ] || { mknod kmsg c 2 11 && chmod 600 kmsg; } || die

for x in 0 1 2 3
do
        # These devices are for initial serial console
        ! [ -c ttyS${x} ] && rm -rf ttyS${x}
        [ -e ttyS${x} ] || { mknod ttyS${x} c 4 $(( 64 + $x )) && chmod 600 ttyS${x}; } || die
        # These devices are used for initial ttys - good to have
        ! [ -c tty${x} ] && rm -rf tty${x}
        [ -e tty${x} ] || { mknod tty${x} c 4 $x && chmod 666 tty${x}; } || die

done

[ -d fd ] || ln -svf /proc/self/fd fd || die
[ -L stdin ] || ln -svf /proc/self/fd/1 stdin || die
[ -L stdout ] || ln -svf /proc/self/fd/1 stdout || die
[ -L stderr ] || ln -svf /proc/self/fd/2 stderr || die
[ -L core ] || ln -svf /proc/kcore core || die
