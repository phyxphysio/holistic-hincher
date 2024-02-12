from playwright.sync_api import Page, expect


def test_give_feedback(page: Page, domain) -> None:
    page.goto(domain)
    page.get_by_role("link", name="Feedback").click()
    page.get_by_label("Name:").click()
    page.get_by_label("Name:").fill("test")
    page.get_by_label("Email:").click()
    page.get_by_label("Email:").fill("test@test.com")
    page.get_by_label("How satisfied were you with the overall cleaning service provided?").select_option("very satisfied")
    page.get_by_label("How would you rate the cleanliness of your space after the cleaning?").select_option("excellent")
    page.get_by_label("Did the cleaner follow any specific instructions or requests you had given?").select_option("yes")
    page.get_by_label("Areas for improvement:").select_option("dusting/vaccumming")
    page.get_by_label("Areas of satisfaction:").select_option("dusting/vaccumming")
    page.get_by_label("Would you recommend our cleaning services to others?").select_option("maybe")
    page.get_by_label("Is there anything else you would like to share about your experience with our cleaning service?").click()
    page.get_by_label("Is there anything else you would like to share about your experience with our cleaning service?").fill("Great lean ")
    page.get_by_label("Please provide your contact information if you would like us to follow up with you regarding your feedback:").click()
    page.get_by_label("Please provide your contact information if you would like us to follow up with you regarding your feedback:").fill("Great clean ")
    page.goto(f"{domain}/success")
    page.context.close()

