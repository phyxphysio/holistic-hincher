from playwright.sync_api import Page, expect

def test_create_subscriber(page: Page, domain) -> None:
    
    page.goto(domain)
    page.get_by_role("link", name="Log In").click()
    page.get_by_label("Username:").click()
    page.get_by_label("Username:").fill("test_member")
    page.get_by_label("Password:").click()
    page.get_by_label("Password:").fill("123test123")
    page.get_by_role("button", name="Log In").click()
    page.get_by_role("link", name="Subscribe").nth(1).click()
    page.get_by_label("Email").click()
    page.get_by_label("Email").fill("test@test.com")
    page.get_by_placeholder("1234 1234 1234 1234").click()
    page.get_by_placeholder("1234 1234 1234 1234").fill("4242 4242 4242 4242")
    page.get_by_placeholder("MM / YY").click()
    page.get_by_placeholder("MM / YY").fill("03 / 45")
    page.get_by_placeholder("Full name on card").click()
    page.get_by_placeholder("Full name on card").fill("Tester")
    page.get_by_test_id("hosted-payment-submit-button").click()
    page.get_by_placeholder("CVC").click()
    page.get_by_placeholder("CVC").fill("200")
    page.get_by_test_id("hosted-payment-submit-button").click()
    page.get_by_text("See Member Resources").click()    

    page.close()
