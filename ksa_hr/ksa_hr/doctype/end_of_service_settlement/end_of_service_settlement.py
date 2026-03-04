# Copyright (c) 2026, Prajakta and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import getdate


class EndofServiceSettlement(Document):

    def before_save(self):
        if self.date_of_joining and self.last_working_date:
            doj = getdate(self.date_of_joining)
            lwd = getdate(self.last_working_date)

            years = (lwd - doj).days / 365
            self.years_of_service = round(years, 2)

            basic = self.basic_salary or 0

            # KSA EOS Rule
            if years < 2:
                eos = 0
            elif years <= 5:
                eos = (basic / 2) * years
            else:
                eos = basic * years

            self.eos_amount = round(eos, 2)
