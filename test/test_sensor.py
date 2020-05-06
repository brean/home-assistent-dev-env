# we use the normal Web Interface to logg in and execute our tests
# alternative would be: https://www.home-assistant.io/integrations/rest/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


LOVELACE_USERNAME='user'
LOVELACE_PASSWORD='1234'
# This should be the nginx-docker container name, see docker-compose file.
LOGIN_URL='http://nginx'
HASS_STARTUP_TIME=20


def setup():
    """Start headless Chrome in docker container."""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    # wait for home-assistant to start up
    driver.implicitly_wait(HASS_STARTUP_TIME)
    return driver


def expand_shadow_element(driver, element):
    """Small workaround to get the shadowRoot element using JS."""
    return driver.execute_script('return arguments[0].shadowRoot', element)


def get_from_shadow(driver, elem, qry):
    for q in qry:
        elem = elem.find_element_by_css_selector(q)
        elem = expand_shadow_element(driver, elem)
    return elem


def login(driver, user=LOVELACE_USERNAME, passwd=LOVELACE_PASSWORD):
    """execute login on main page."""
    driver.get(LOGIN_URL)
    qry = [
        'ha-authorize',
        'ha-auth-flow',
        'ha-form'
    ]
    ha_form = get_from_shadow(driver, driver, qry)

    inner_forms = ha_form.find_elements_by_tag_name('ha-form')
    assert len(inner_forms) == 2
    user_form, pw_form = inner_forms

    qry = ['ha-form-string']
    user_form = expand_shadow_element(driver, user_form)
    user_input = get_from_shadow(driver, user_form, qry)
    user_input = user_input.find_element_by_css_selector('paper-input')
    user_input.send_keys(LOVELACE_USERNAME)

    pw_form = expand_shadow_element(driver, pw_form)
    pass_input = get_from_shadow(driver, pw_form, qry)
    pass_input = pass_input.find_element_by_css_selector('paper-input')
    pass_input.send_keys(LOVELACE_PASSWORD)

    pass_input.send_keys(Keys.RETURN)


def test_sensor():
    driver = setup()
    login(driver)

    qry = [
        'home-assistant',
        'home-assistant-main',
        'app-drawer-layout partial-panel-resolver ha-panel-lovelace',
        'hui-root',
        'ha-app-layout#layout div#view hui-view'
    ]
    hui_view = get_from_shadow(driver, driver, qry)
    badges_container = hui_view.find_element_by_css_selector('div#badges')
    badges = badges_container.find_elements_by_css_selector('hui-state-label-badge')

    found_sensor = None

    for badge in badges:
        badge = expand_shadow_element(driver, badge)
        badge_label = get_from_shadow(driver, badge, ['ha-state-label-badge'])
        sensor = badge_label.find_elements_by_css_selector('ha-label-badge.sensor')
        if not sensor:
            continue

        sensor = expand_shadow_element(driver, sensor[0])
        sensor_value = sensor.find_element_by_css_selector('div.value span')
        found_sensor = int(sensor_value.text) == 23

    assert found_sensor, 'sensor not found in badges'
    

