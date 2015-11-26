# -*- coding: utf-8 -*-
import os
from time import time, gmtime, strftime

from mago.test_suite.solaris_gnome_about_me import GnomeAboutMeTestSuite 

class SolarisGnomeAboutMeTests(GnomeAboutMeTestSuite):
    
    #define values for the texts inside the about me dialog.
    contact_values = { "txtAIM/iChat" : "299010@190019.net",
               "txtGroupwise" : "9190190190@91091901901.com",
               "txtHome" : "119111@91191919.com",
               "txtHome1" : "0191939102",
               "txtICQ" : "89123281290",
               "txtMSN" : "912101@91090.com",
               "txtMobile" : "1231313132132",
               "txtWork" : "91929010921@9019191.com",
               "txtWork1" : "n odio. Donec sollicitudin posuere, odio. Nam eu sodal",
               "txtWorkfax" : "1290390190",
               "txtJabber" : "9012391290@90191901.com",
               "txtYahoo" : "901921901901@01219191.com"
               }

    address_values = { "txtAddress" : "742 Evergreen Terrace",
               "txtAddress1" : "bibendum, urna sem ipsum, ultricies a, imperdiet ut, ligula. Cras tempus enim",
               "txtCity" : "Springfield",
               "txtCity1" : "Santiago",
               "txtCountry" : "Pitcairn Islands",
               "txtCountry1" : "Monaco",
               "txtPObox" : "9193910919129",
               "txtPObox1" : "9190190190910",
               "txtState/Province" : "Adamstown",
               "txtState/Province1" : "Bounty Bay",
               "txtZip/Postalcode" : "123456789",
               "txtZip/Postalcode1" : "987654321"
               }

    personal_values = { "txtAssistant" : "John Doe",
               "txtCalendar" : "123",
               "txtCompany" : "Springfield Nuclear Power Plant",
               "txtDepartment" : "digr gal-gal-gu-ne-ra",
               "txtHomepage" : "bloh@blah.com",
               "txtManager" : "fringilla sollicitudin, odio at libero. Aliquam in massa non nunc. Sed males",
               "txtProfession" : "spendisse diam. Pellentesque scelerisque vel, lacinia quam at arcu turpis non tincidunt rutrum molesti",
               "txtTitle" : "se platea dictumst. Duis ut mauris mattis eget, bibendum leo, aliquet tincid",
               "txtWeblog" : "iam. Pellentesque scelerisque vel, lacinia quam"
               }

    
    def change_text_values(self):
        self.application.select_tab('Contact')
        self.application.file_values(self.contact_values)
        self.application.select_tab('Address')
        self.application.file_values(self.address_values)
        self.application.select_tab('PersonalInfo')
        self.application.file_values(self.personal_values)
        self.application.close()
        #Re open the window and check if the values presented
        #to the users are the ones we added before.
        #if they are not the check_values method will raise an exception.
        self.application.open()

        self.application.select_tab('Contact')
        self.application.check_values(self.contact_values)
        self.application.select_tab('Address')
        self.application.check_values(self.address_values)
        self.application.select_tab('PersonalInfo')
        self.application.check_values(self.personal_values)

    def change_picture_to_png(self, photo_path):
	path = os.path.join(self.get_test_dir(), photo_path)
        self.application.change_picture(path)

    def change_picture_to_svg(self, photo_path):
	path = os.path.join(self.get_test_dir(), photo_path)
        self.application.change_picture(path)
    
    def clean_up_fields_and_picture(self):
        self.application.change_picture_to_default()

        self.application.select_tab('Contact')
        self.application.clean_up_text_values(self.contact_values)
        self.application.select_tab('Address')
        self.application.clean_up_text_values(self.address_values)
        self.application.select_tab('PersonalInfo')
        self.application.clean_up_text_values(self.personal_values)
    
if __name__ == "__main__":
    solaris_gnome_about_me_test =  SolarisGnomeAboutMeTests()
    solaris_gnome_about_me_test.run()
