#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/binary_info.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"

const uint LED_PIN = 25;

int main()
{
    stdio_init_all();

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    // GPIO 16 (PWM A) and 17 (PWM B) are allocated as PWM
    gpio_set_function(16, GPIO_FUNC_PWM);
    gpio_set_function(17, GPIO_FUNC_PWM);

    // Find out which PWM slice is connected to GPIO 16 (Slice 0)
    uint slice = pwm_gpio_to_slice_num(16);

    // Set Free running mode, , int 1, frac 4 and channel B inverted for Slice 0
    pwm_set_clkdiv_mode(slice, PWM_DIV_FREE_RUNNING);
    // Set No phase correct
    pwm_set_phase_correct(slice, false);
    // Sets the Integer and Iractional part for the clock divider
    pwm_set_clkdiv_int_frac(slice, 1, 0);
    //pwm_set_clkdiv_int_frac(slice, 8, 4);
    // Sets A and B output polarity
    pwm_set_output_polarity(slice, false, false);

    // Set the TOP register to 832, which with the system frequency at 125MHz, 
    // corresponds to a frequency of 150KHz for PWM with Div Int at 1 and Div Frac at 0
    pwm_set_wrap(slice, 832);
    // Set the TOP register to 100, which with the system frequency at 125MHz, 
    // corresponds to a frequency of 150KHz for PWM with Div Int at 8 and Div Frac at 4
    //pwm_set_wrap(slice, 100);
    // Set levels of counter for A and B output, to have 50% duty cycle
    pwm_set_both_levels(slice, 416, 416);
    //pwm_set_both_levels(slice, 50, 50);

    // Enable PWM running
    pwm_set_enabled(slice, true);

    uint32_t clockHz = clock_get_hz(clk_sys);
    printf("clk_sys: %dHz\n", clockHz);

    while (1)
    {
        gpio_put(LED_PIN, 1);
        sleep_ms(300);
        gpio_put(LED_PIN, 0);
        sleep_ms(300);
    }
}