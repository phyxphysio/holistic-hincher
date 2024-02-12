from playwright.sync_api import Page, expect


def test_get_clean(page: Page, domain) -> None:
    page.goto(domain)
    page.get_by_role("button", name="Get a clean").click()
    page.get_by_label("First name:").click()
    page.get_by_label("First name:").fill("test")
    page.get_by_label("First name:").press("Tab")
    page.get_by_label("Last name:").fill("test@test")
    page.get_by_label("Last name:").press("Tab")
    page.get_by_label("Last name:").dblclick()
    page.get_by_label("Last name:").click(click_count=3)
    page.get_by_label("Last name:").press("Meta+x")
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("test@test")
    page.get_by_label("Last name:").click()
    page.get_by_label("Last name:").fill("test")
    page.get_by_label("Mobile:").click()
    page.get_by_label("Mobile:").fill("12345869")
    page.get_by_label("Street Address of the property:").click()
    page.get_by_label("Street Address of the property:").fill("123 Manly drive, manly")
    page.get_by_label("Post code:").click()
    page.get_by_label("Post code:").fill("1234")
    page.get_by_text("House", exact=True).click()
    page.get_by_text("Fortnightly").click()
    page.get_by_label("How many bedrooms in the home?").select_option("1-2 bed")
    page.get_by_label("How many people use the office?").select_option("11-15 people")
    page.get_by_text("Meal Preparation").click()
    page.get_by_label("Additonal information:").click()
    page.get_by_label("Additonal information:").fill("Looking forward to it")
    page.get_by_role("button", name="Send Enquiry").click()
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("test@test.com")
    page.get_by_role("button", name="Send Enquiry").click()
    page.context.close()

