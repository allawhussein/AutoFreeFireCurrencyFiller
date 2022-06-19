from selenium import webdriver #this is needed to basicly anything
from selenium.webdriver import ActionChains #this used to open some hover menus
from selenium.webdriver.support import expected_conditions as EC #this is used to prevent the driver form clicking unloaded elements
from selenium.webdriver.common.by import By #this used for element finding method
from selenium.webdriver.common.keys import Keys #this is used to simiulate keyboard keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import os
import time

from services.variables import *
from services import alcaptain_services
from services import razer_gold_services
from services import telegram_services
from services import free_fire_razer

def free_fire_bot_init(driver):
    print("Free Fire Bot v0.1")
    initialize_variables()

    if (driver == None):
        driver = webdriver.Firefox()
    driver.execute_script('window.open("https://gold.razer.com/gold/catalog/","_blank");')

    return driver
    

def free_fire_bot(driver, razer_driver, counter):
    credentials = razer_accounts[counter]
    print("MainCode: using razer account: " + credentials[0])
    try:
        order = None
        alcaptain_services.get_alcaptain_main_page(driver, driver.window_handles[0])
        try:
            order_clicked = alcaptain_services.quick_accept_all_eligible_orders(driver, driver.window_handles[0])
        except:
            pass
        order = alcaptain_services.select_order(driver, driver.window_handles[0])
        print("MainCode-DEBUG: ", order)
        if order != None:
            login_succes = free_fire_razer.razer_sign_in_usa_fix(driver, driver.window_handles[1], credentials)
            if login_succes == 1:
                result = free_fire_razer.pay_order(driver, driver.window_handles[1], order[2], str(int(order[1])))#the double conversion is to eliminate and spaces
                if result[0] == 1:
                    razer_url = result[1]
                    login_success = razer_gold_services.razer_gold_login(razer_driver, razer_driver.window_handles[0], credentials, razer_url)
                    if login_success == 1:
                        balance = razer_gold_services.razer_gold_check_balance(razer_driver, razer_driver.window_handles[0], 1)
                        if balance == "G":
                            print("Main Code: archiving order")
                            archive(str(order[0]))
                            #transaction_id = razer_gold_services.razer_gold_proceed_to_check_out(razer_driver, razer_driver.window_handles[0], credentials)
                            #transaction_id = "R"
                            transaction_id = "NONE - Test Case By Hussein Allaw"
                            if transaction_id == None:
                                print("Main Code: transaction id is not obtained, enter any thing to continue the bot")
                                x = input()
                                return [driver, counter]
                            elif transaction_id == "R":
                                print("Main Code: Simply Restarting")
                            elif transaction_id == "S":
                                print("Main Code: Bot will be Stoped")
                                raise Exception
                            else:
                                reply_message = "The FreeFire ID: " + str(order[1]) + "\nThe Transaction ID: " + str(transaction_id) + datetime.now().strftime("\nDate & Time: %d-%m-%Y -- %H:%M")
                                alcaptain_services.successful_order_reply(driver, driver.window_handles[0], reply_message)
                                telegram_services.send_msg("💎Free Fire Order Payed by Free Fire Bot\nThe Order ID: " + order[0].split("#")[1] + "\nThe FreeFire ID: " + str(order[1]) + "\nThe Transaction ID: " + str(transaction_id) + datetime.now().strftime("\nDate and Time: %d-%m-%Y -- %H:%M"))
                        elif balance == "C":
                            counter += 1
                            print("Main Code: changing account")
                            if (counter > len(razer_accounts)):
                                counter = 0
                            credentials = razer_accounts[counter]
                            rewrite_accounts(counter)
                            print("Main Code: now using : " + credentials[0])
                            razer_driver = razer_gold_services.razer_gold_sign_out(razer_driver, razer_driver.window_handles[0])
                            print("insufficient funds, signing out, and restarting process")
                        elif balance == "R":
                            pass
                        else:
                            print("Main Code: Unkown Choice Inputed in RGS.RGCB service")
                            assert False
                    else:
                        print("Main Code: Login to Razer payment portal is unsuccessful")
                elif result[0] == 2:
                    alcaptain_services.failed_order_reply(driver, driver.window_handles[0], "The Free Fire ID " + str(order[1]) + " is invalid (rejected by Free Fire Company)")
                    telegram_services.send_msg("Free Fire Order Rejected\nOrder ID: " + order[0].split("#")[1] + "\nFree Fire ID: " + str(order[1]) + datetime.now().strftime("\nDate and Time: %d-%m-%Y -- %H:%M") + "\nRejected by Razer Website")
                    """elif result[0] == 4:
                        if repetitive_order[1] > 0:
                            repetitive_order[1] -= 1"""
                else:
                    print("Main Code: Razer URL is not obtained, simply restarting")
        elif order == None:
            temp_sus_orders_list = alcaptain_services.get_list_of_active_archived_orders(driver, driver.current_window_handle)
            for order in temp_sus_orders_list:
                if order not in sus_orders_list:
                    sus_orders_list.append(order)
                    print(" -MainCode: sending sus order to telegram group")
                    telegram_services.send_msg("AlCaptain ID:%20" + order[0].split("#")[1] + "%0D%0Ahis PUBG ID:+" + order[1] + "%0D%0Ais sus, error ❌")
    except Exception as error_message:
        print("MainCode: sending error message to Hussein Allaw")
        print(error_message)
        telegram_services.send_msg_dev(repr(error_message))
    except KeyboardInterrupt:
        print("MainCode: program ended by user")
        return None
    return [driver, counter]

if __name__ == "__main__":
    driver = free_fire_bot_init(None)
    razer_driver = webdriver.Firefox()
    counter = 0
    while driver != None:
        driver, counter = free_fire_bot(driver, razer_driver, counter)