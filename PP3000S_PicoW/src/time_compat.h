#ifndef TIME_COMPAT_H
#define TIME_COMPAT_H

#include <pico/util/datetime.h>

#if defined(PICO_RP2350)
#include "hardware/powman.h"
#define rp_time_init() powman_init()
#define rp_time_set_datetime(t) powman_set_datetime(t)
#define rp_time_get_datetime(t) powman_get_datetime(t)
#define rp_time_set_alarm(t, cb) powman_set_alarm(t, cb)
#else
#include "hardware/rtc.h"
#define rp_time_init() rtc_init()
#define rp_time_set_datetime(t) rtc_set_datetime(t)
#define rp_time_get_datetime(t) rtc_get_datetime(t)
#define rp_time_set_alarm(t, cb) rtc_set_alarm(t, cb)
#endif

#endif // TIME_COMPAT_H
