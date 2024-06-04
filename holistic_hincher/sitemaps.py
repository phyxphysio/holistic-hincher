# sitemaps.py

from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5  
    changefreq = "monthly"  

    def items(self):
        return [
            "home",
            "about",
            "cleaning_services",
            "feedback",
            "member_resources",
            "login",
            "change_password",
            "password_reset",
            "signup",
            "memberships"
        ]  

    def location(self, item):
        return reverse(item)
