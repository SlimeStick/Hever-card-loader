import argparse
from dataclasses import dataclass
from time import sleep

import pyautogui

DEFAULT_IMAGE_SEARCH_CONFIDENCE = 0.9
CRITICAL_IMAGE_SEARCH_CONFIDENCE = 0.99
HEVER_MINIMUM_LOAD_VALUE: int = 5  # Sadly the loading system only accepts integers larger than 5
HEVER_MAXIMUM_LOAD_VALUE: int = 1000
HEVER_MAXIMUM_DAILY_LOAD_COUNT = 5


def press_image(image_path: str, confidence: float = DEFAULT_IMAGE_SEARCH_CONFIDENCE):
    image_location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    image_x, image_y = pyautogui.center(image_location)
    pyautogui.click(image_x, image_y)


def enter_field(field_image_path: str, text: str, remove_previous_data: bool):
    press_image(field_image_path)

    if remove_previous_data:
        pyautogui.hotkey('ctrl', 'a')

    pyautogui.typewrite(text)


def load_once(amount: int, card_number: str, year: str, month: str, cvv: str):
    # go to the checkout site
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite("https://www.hvr.co.il/orders/gift_2000.aspx")
    pyautogui.press("enter")

    # wait for page to load
    sleep(5)

    enter_field("amount_to_load.png", str(amount), True)

    # accept the EULA
    pyautogui.press('tab')
    pyautogui.press('space')

    enter_field("card_number.png", card_number, True)
    enter_field("card_year.png", year, False)
    enter_field("card_month.png", month, False)
    enter_field("card_cvv.png", cvv, True)

    # go off the fields so that the card can be checked
    pyautogui.press('tab')

    # wait for the card to be checked
    sleep(5)

    # submit
    pyautogui.press('tab')
    pyautogui.press('space')

    # wait for confirmation popup to show up
    sleep(3)
    press_image("final_accept_button.png", confidence=CRITICAL_IMAGE_SEARCH_CONFIDENCE)


def log_into_hever():
    # go to the hever site
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite("https://www.hvr.co.il/")
    pyautogui.press("enter")
    # wait for autofill
    sleep(3)
    # choose the first option
    pyautogui.press('down')
    pyautogui.press('enter')
    # submit the log-in form
    pyautogui.press('enter')


def open_browser():
    # open the best browser there is
    pyautogui.press('win')
    pyautogui.typewrite('brave')
    pyautogui.press('enter')
    # wait for app to open
    sleep(3)
    pyautogui.press('tab')
    pyautogui.press('space')
    # open new tab incase browser was already open
    pyautogui.hotkey('ctrl', 't')


def hvr_floor_function(value: float):
    return int(value + 0.5)


@dataclass(frozen=True, order=True)
class LoadOption:
    discount: float
    load_value: int


def calculate_ideal_load_option(current_discount: float):
    load_options = [
        LoadOption(
            discount=1 - hvr_floor_function((1 - current_discount) * load_value) / load_value,
            load_value=load_value,
        )
        for load_value in range(HEVER_MINIMUM_LOAD_VALUE, HEVER_MAXIMUM_LOAD_VALUE + 1)
    ]
    ideal_load_option = max(load_options)
    return ideal_load_option


def build_parser():
    parser = argparse.ArgumentParser(description="Auto-fill HVR payment forms using image recognition to automate"
                                                 "manual repeated low amount inputs to get "
                                                 "a higher discount percentage")
    parser.add_argument("--load-count", required=True, type=int,
                        help=f"The amount of times to load. Choosing {HEVER_MAXIMUM_DAILY_LOAD_COUNT} makes it so you"
                             f"cannot use the card today anymore.")
    parser.add_argument("--current-discount-percentage", required=True, type=float,
                        help="Your current hever discount percentage. Varies with the amount already spent on the "
                             "card, during holidays and birthday months.")
    parser.add_argument("--card-number", required=True, type=str, help="Card number")
    parser.add_argument("--year", required=True, type=str, help="Card expiration year")
    parser.add_argument("--month", required=True, type=str, help="Card expiration month")
    parser.add_argument("--cvv", required=True, type=str, help="Card CVV")
    return parser


def main():
    args = build_parser().parse_args()

    load_option = calculate_ideal_load_option(float(args.current_discount_percentage))
    print(f"Going to load the value {load_option.load_value} "
          f"for {args.load_count} times with a discount of {load_option.discount}")

    for i in range(args.load_count):
        open_browser()

        log_into_hever()

        load_once(load_option.load_value, args.card_number, args.year, args.month, args.cvv)
        # Wait to not spam the website
        sleep(60)


if __name__ == "__main__":
    main()
