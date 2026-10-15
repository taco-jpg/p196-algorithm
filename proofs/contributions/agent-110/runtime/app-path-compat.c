#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/* Container compatibility only: use the readable alias for this process's
 * executable. No compiler, library, theorem, or object-file bytes are changed.
 * Every other readlink request is forwarded unchanged to the real libc call.
 */
ssize_t readlink(const char *path, char *buffer, size_t size) {
    typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
    readlink_fn real_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (!real_readlink) { errno = ENOSYS; return -1; }
    char own_exe[64];
    int length = snprintf(own_exe, sizeof own_exe, "/proc/%ld/exe", (long)getpid());
    if (length > 0 && (size_t)length < sizeof own_exe && strcmp(path, own_exe) == 0)
        return real_readlink("/proc/self/exe", buffer, size);
    return real_readlink(path, buffer, size);
}
