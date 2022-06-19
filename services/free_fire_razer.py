from selenium import webdriver #this is needed to basicly anything
from selenium.webdriver import ActionChains #this used to open some hover menus
from selenium.webdriver.support import expected_conditions as EC #this is used to prevent the driver form clicking unloaded elements
from selenium.webdriver.common.by import By #this used for element finding method
from selenium.webdriver.common.keys import Keys #this is used to simiulate keyboard keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from services.variables import *
import time
import services.telegram_services as telegram_services
from selenium.webdriver.support.ui import WebDriverWait

def mini_razer_function(driver, choice):
    try:
        for a_tag in driver.find_elements_by_tag_name("a"):
            try:
                if a_tag.get_attribute("href") == "javascript: void(0)" and a_tag.text != "Return to Catalog":
                    a_tag.click()
                    time.sleep(0.5)
                    if choice:
                        mini_razer_function(driver, choice)
            except:
                pass
    except:
        mini_razer_function(driver, choice)

def razer_sign_in_usa_fix(driver, window_handle, credentials):
    driver.switch_to.window(window_handle)
    time_zero = time.time()
    print(" -RSI-USAFIX: Checking if we are logged in")
    loop_counter = 1
    while time.time() - time_zero < time_of_waiting:#first to loop to check/login
        #print(" -RSI-USAFIX: Loop ", loop_counter," time remaining ", str(20 - time.time() + time_zero)[:5])
        loop_counter += 1
        try:#checking if login button is present
            if (len(driver.find_element_by_tag_name("nav").find_elements_by_link_text("LOG IN"))):
                print(" -RSI-USAFIX: Pressing Login Button")
                driver.find_element_by_tag_name("nav").find_element_by_link_text("LOG IN").click()
        except:
            pass
        
        try:#check if we are logged in anyways
            if "razerid" not in driver.current_url and credentials[0] in driver.find_element_by_class_name("profile-info").text:#check if we are logged in or not
                if "freefire" not in driver.current_url:
                    print(" -RSI-USAFIX: correct account signed in, loading freefire page")
                    driver.get("https://gold.razer.com/gold/catalog/freefire-direct-top-up")
                    return 1
                print(" -RSI-USAFIX: We are signed in")
                return 1
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-USAFIX-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except:
            pass

        try:#changing accounts
            if "razerid" not in driver.current_url and len(driver.find_elements_by_class_name("profile-info")) and driver.find_element_by_class_name("profile-info").text != "" and credentials[0] not in driver.find_element_by_class_name("profile-info").text:# clicking sign Out
                print(" -RSI-USAFIX: not logged in with the correct account")
                print(" -RSI-USAFIX-DEBUG: account name: ", credentials[0], ", element text: ", driver.find_element_by_class_name("profile-info").text)
                driver.find_element_by_class_name("component-profile").click()
                driver.find_element_by_link_text("Sign Out").click()
                print(" -RSI-USAFIX: Signing Out")
            elif "razerid" not in driver.current_url:
                driver.find_element_by_class_name("component-profile").click()
                if len(driver.find_elements_by_link_text("SIGN IN")):
                    print(" -RSI-USAFIX: account name holder is not found, pressign SIGN IN")
                    driver.find_element_by_link_text("SIGN IN").click()
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-USAFIX-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except:
            pass

        for button in driver.find_elements_by_tag_name("button"):#check if other accoutns are cached (it will just click use another account)
            if button.text.lower() == "connect with another account":
                button.click()
                break

        try:#input login creedentials and press login button
            if driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[1]/input").get_attribute("value") != credentials[0] and "razerid" in driver.current_url:
                print(" -RSI-USAFIX: entering the username ", credentials[0])
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[1]/input").send_keys(Keys.CONTROL + "a")
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[1]/input").send_keys(Keys.DELETE)
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[1]/input").send_keys(credentials[0])
            if driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[2]/input").get_attribute("value") != credentials[1] and "razerid" in driver.current_url:
                print(" -RSI-USAFIX: entering the password ", "*"*len(credentials[1]))
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[2]/input").send_keys(Keys.CONTROL + "a")
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[2]/input").send_keys(Keys.DELETE)
                driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/form/div[2]/input").send_keys(credentials[1])
            if driver.execute_script('return document.readyState;') == 'complete' and "razerid" in driver.current_url:
                print(" -RSI-USAFIX: pressing log in")
                driver.execute_script("arguments[0].click();", driver.find_element_by_id("btn-log-in"))
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-USAFIX-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except NoSuchElementException:
            pass
        except Exception as error:
            print(" -RSI-USAFIX-DEBUG<Login Form>: ", error)

        while driver.execute_script('return document.readyState;') != 'complete' or len(driver.find_elements_by_class_name("component-page-loader")):
            time_zero = time.time()
        for wee in driver.find_elements_by_id("login"):
            try:#just in case the wee element is no more attached to DOM
                if "Loading..." in wee.text or "Logging you in..." in wee.text:
                    time_zero = time.time()
                    break
            except:
                pass
    
    if not len(driver.find_element_by_class_name("profile-info")) or not len(driver.find_element_by_class_name("component-profile")):
        print(" -RSI-USAFIX: Account Info button class names have been changed, the code needs an update contact Hussein Allaw")

    return 2

def razer_sign_in(driver, window_handle, credentials):#redundant?#["alcaptain.usa16@gmail.com", "112233jj"]
    #return 1 if successful login
    #return 2 if login timeout
    dialog_close_css_selector = ".dialog-item-cta > a:nth-child(1)"
    sign_in_button_css_selector = "#webshop_step_1 > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2)"
    login_email_field_css_selector = "div.input-container:nth-child(4) > input:nth-child(1)"
    login_password_field_css_selector = "div.input-container:nth-child(5) > input:nth-child(1)"
    login_button_css_selector = "#btn-log-in"
    loading_css_selector = "#login > div.absolute.v-center > div"
    user_id_css_selector = "#PlayerId147"
    
    driver.switch_to.window(window_handle)
    free_fire_url = "https://gold.razer.com/gold/catalog/freefire-direct-top-up"
    while driver.execute_script('return document.readyState;') != 'complete':
        pass
    if razer_sign_in_usa_fix(driver, window_handle, credentials) == 2:
        return 2

    print(" -RSI: Free Fire Razer site is loaded")
    zero_time = time.time()
    credentials_filled = False

    while time.time() - zero_time < 20:
        mini_razer_function(driver, False)
        try:#pressing sign in button
            driver.find_element_by_css_selector(sign_in_button_css_selector).click()
            zero_time = time.time()
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except:
            pass
        else:
            print(" -RSI: pressed the sign in button")
        try:#check if sign is required again after long time
            for a_tag in driver.find_elements_by_tag_name("a"):
                if a_tag.text == "SIGN IN":
                    a_tag.click()
                    time_zero = time.time()
                    print(" -RSI: Sign is required another time")
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except Exception as err:
            print(" -RSI<DEBUG>: ", err)
        try:#filling credentials
            driver.find_element_by_css_selector(login_email_field_css_selector).clear()
            driver.find_element_by_css_selector(login_email_field_css_selector).send_keys(credentials[0])
            driver.find_element_by_css_selector(login_password_field_css_selector).clear()
            driver.find_element_by_css_selector(login_password_field_css_selector).send_keys(credentials[1])
            print(" -RSI: filled form credentials")
            driver.find_element_by_css_selector(login_button_css_selector).click()
            print(" -RSI: pressing sign in")
            zero_time = time.time()
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except:
            pass
        else:
            credentials_filled = True
        try:#checking if user id field is visible or not
            for label in driver.find_element_by_id("webshop_step_1").find_elements_by_tag_name("label"):
                assert "User ID" in label.text
                driver.find_element_by_id(label.get_attribute("for"))
                assert driver.find_element_by_id(label.get_attribute("for")).is_enabled()
                break
            else:
                assert False
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except Exception as err:
            pass
        else:
            print(" -RSI: login is successful, RSI is over")
            return 1
        try:#checking if loading window is open
            assert "Loading" in driver.find_element_by_css_selector(loading_css_selector).text
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except:
            pass
        else:
            zero_time = time.time()
        try:#if login portal was cached
            assert not credentials_filled
            for button in driver.find_elements_by_tag_name("button"):
                if "ANOTHER ACCOUNT" in button.text:
                    button.click()
                    break
            else:
                assert False
        except ElementClickInterceptedException as err_message:
            err_message = str(err_message)
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -RSI-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
        except:
            pass
        else:
            print(" -RSI: cached account is found, clicking other")
            time_zero = time.time()
        if driver.execute_script('return document.readyState;') != 'complete':
            time_zero = time.time()
    print(" -RSI: signing in timeout, RSI is over")
    return 2

def pay_order(driver, window_handle, offer, player_id, retry_attempts_left = 1):
    #return 1 & order url if successful.
    #return 2 if FreeFire ID is wrong.
    #return 3 if exact order is not found.
    #return 4 if Razer Gold payment method is not found
    #return 5 if Checout button is not found
    #restart function if user id field is disabled
    #return 7 for unknown error & the place of it
    #return 8 if user id is invalid
    print(" -PO: pay_order services is initiated")
    try:
        player_id = int(player_id)
    except:
        print(" -PO: player id is invalid, returning '8'")
        return (8, 0)
    else:
        pass
    user_id_box_id = "webshop_step_user_info"
    user_id_css_selector = "#gameUserId155"
    card_class_name = "selection-tile"
    card_box_css_selector = "#webshop_step_sku"
    payment_method_box_css_selector = "#webshop_step_payment_channels"
    checkout_box_css_selector = "#webshop_step_summary"
    error_box_css_selector = "#error"
    driver.switch_to.window(window_handle)
    
    mini_razer_function(driver, True)
    while driver.execute_script('return document.readyState;') != 'complete' or len(driver.find_elements_by_class_name("component-page-loader")):
        pass

    print(" -PO: freefire razer top up page is loaded")
    try:
        for label in driver.find_element_by_id(user_id_box_id).find_elements_by_tag_name("label"):
            if "User ID" in label.text:
                user_id_field = driver.find_element_by_id(label.get_attribute("for"))
                assert user_id_field.is_enabled()
                if user_id_field.get_attribute("value") != str(player_id):
                    user_id_field.send_keys(Keys.CONTROL + "a")
                    user_id_field.send_keys(Keys.DELETE)
                    user_id_field.send_keys(player_id)
                    print(" -PO: entering player id")
                break
        else:
            assert False
    except ElementClickInterceptedException as err_message:
        print(" -PO-DEBUG: element need to be hidden")
        tag = err_message.split("another element ")[1].split(" obscures it")[0]
        html_tag = tag[1:].split(" ")[0]
        css_class = tag.split('class="')[1].split('"')[0]
        for target_tag in driver.find_elements_by_tag_name(html_tag):
            if target_tag.get_attribute("class") == css_class:
                driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                print(" -PO-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                break
        print(" -PO-DEBUG: element need to be hidden")
    except Exception as err:#return 6 or 7
        if "Element is disabled" in str(err) or "Assertion Error" in str(err):
            driver.refresh()
            print(" -PO: player id is disabled, reloading page")
            telegram_services.send_msg_dev("-FreeFire Bot - free_fire_razer: postion 1, error 7")
            telegram_services.send_msg_dev(str(err))
            return pay_order(driver, window_handle, offer, player_id)
        print(" -PO-DEBUG: ", err)
    else:
        pass
    
    try:#searching for offer
        for card in driver.find_element_by_css_selector(card_box_css_selector).find_elements_by_class_name(card_class_name)[::-1]:
            if int(card.text.split(" +")[0]) == offer:
                card.click()
                print(" -PO: bundle is chosen")
                break
            elif "+" in card.text and int(card.text.split(" + ")[0]) + int(card.text.split(" + ")[1].split(" ")[0]) == offer:
                card.click()
                print(" -PO: bundle is chosen")
                break
        else:#return 3
            print(" -PO: no suitable offer was found, returning 3")
            return (3, 0)
    except Exception as err:
        print(" -PO-DEBUG: ", err)

    print(" -PO: clicking the Razer Gold payment method")   
    if len(driver.find_elements_by_css_selector(payment_method_box_css_selector)): 
        for payment_method_card in driver.find_element_by_css_selector(payment_method_box_css_selector).find_elements_by_class_name(card_class_name):
            if "Razer Gold" in payment_method_card.text:
                payment_method_card.click()
                print(" -PO: Razer Gold succesfully chosen")
                break
        else:#return 4
            print(" -PO: razer Gold is not availabe, returning 4")
            return (4, 0)
        
    print(" -PO: proceeding to checkout")
    
    if len(driver.find_elements_by_css_selector(checkout_box_css_selector)):
        for button in driver.find_element_by_css_selector(checkout_box_css_selector).find_elements_by_tag_name("button"):
            if "CHECKOUT" in button.text:
                button.click()
                print(" -PO: pressed CHECKOUT button")
                break
        else:#check for checkout button validity
            print(" -PO: checkout is not availabe, returning 5")
            return (5, 0)

    time_zero = time.time()
    while time.time() - time_zero < 120:
        try:#wait for loading to complete
            while "is-loading" in button.get_attribute("class"):
                pass
        except:
            pass
        else:
            pass

        try:#return 1
            assert "gold.razer.com/order/" in driver.current_url
        except:
            pass
        else:
            print(" -PO: successfully obtained the URL, PO is over")
            razer_url = driver.current_url
            driver.switch_to.window(window_handle)
            driver.execute_script("window.open('https://gold.razer.com/gold/catalog/freefire-direct-top-up', '_self')")
            return (1, razer_url)
        
        try:#check for wrong ID message number 2            
            for span in driver.find_elements_by_tag_name("span"):
                if span.text == "Invalid Username/account":
                    if retry_attempts_left:
                        print(" -PO: invalid player id, retrying")
                        driver.refresh()
                        return pay_order(driver, window_handle, offer, player_id, 0)
                    driver.execute_script("window.open('https://gold.razer.com/gold/catalog/freefire-direct-top-up', '_self')")
                    print(" -PO: invalid player id, returning 2")
                    return (2, 0)
        except ElementClickInterceptedException as err_message:
            print(" -PO-DEBUG: element need to be hidden")
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -PO-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
            print(" -PO-DEBUG: element need to be hidden")
        except:
            pass
        
        try:#check for wrong ID message
            assert "Purchase Failed" in driver.find_element_by_css_selector(error_box_css_selector).text
        except ElementClickInterceptedException as err_message:
            print(" -PO-DEBUG: element need to be hidden")
            tag = err_message.split("another element ")[1].split(" obscures it")[0]
            html_tag = tag[1:].split(" ")[0]
            css_class = tag.split('class="')[1].split('"')[0]
            for target_tag in driver.find_elements_by_tag_name(html_tag):
                if target_tag.get_attribute("class") == css_class:
                    driver.execute_script("arguments[0].setAttribute('style','display:none;');", target_tag)
                    print(" -PO-DEBUG: element of tag name: ", html_tag, " and class name: ", css_class, " is hidden by bot")
                    break
            print(" -PO-DEBUG: element need to be hidden")
        except Exception as err:
            pass
        else:
            if retry_attempts_left:
                print(" -PO: invalid player id, retrying")
                driver.refresh()
                return pay_order(driver, window_handle, offer, player_id, 0)
            driver.execute_script("window.open('https://gold.razer.com/gold/catalog/freefire-direct-top-up', '_self')")
            print(" -PO: invalid player id, returning 2, probably non-middle-east id")
            return (2, 0)
        if driver.execute_script('return document.readyState;') != 'complete':
            time_zero = time.time()
    print(" -PO: timeout, returning 7, at postion 0")
    driver.switch_to.window(window_handle)
    driver.execute_script("window.open('https://gold.razer.com/gold/catalog/freefire-direct-top-up', '_self')")
    return (7, 0)
    
def razer_sign_out(driver, window_handle):#redundant?
    account_logo_css_selector = "#__BVID__62"
    account_options_box_css_selector = "div.profile-dropdown-section:nth-child(4)"
    driver.switch_to.window(window_handle)
    driver.find_element_by_css_selector(account_logo_css_selector).click()
    razer_url = driver.current_url
    for button in driver.find_elements_by_tag_name("a"):
        if "Sign Out" in button.text:
            button.click()
            driver.get(razer_url)
            break
    else:
        razer_sign_out(driver, window_handle)

def test_function(driver, window_handle, credentials, offer, player_id):
    credentials = ["alcaptain.usa16@gmail.com", "112233jj"]
    razer_sign_in(driver, window_handle, credentials)
    pay_order(driver, window_handle, offer, player_id)