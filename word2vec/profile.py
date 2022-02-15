class Profession:
    def __init__(self, job_title: str, company: str, dates_employed: str):
        self.job_title = job_title
        self.company = company
        self.dates_employed = dates_employed

    def __str__(self):
        isEmployed = self.dates_employed.split('')  # change wording - if the word Present is available.
        return f"my (__) role is as a {self.job_title} at {self.company}"


class Education:
    def __init__(self, college_name: str, degree_name: str, field_of_study: str, secondary_college_name: str,
                 secondary_degree_name: str, secondary_field_of_study: str):
        self.college_name = college_name
        self.degree_name = degree_name
        self.field_of_study = field_of_study

        self.secondary_college_name = secondary_college_name
        self.secondary_degree_name = secondary_degree_name
        self.secondary_field_of_study = secondary_field_of_study

    def __str__(self):
        """
        --
        depending on the headline, which can include "student" this needs to be changed to studied. Should be
        overridden in headline.
        --
        need to finish up here -- add the secondary college != empty (condition)
        """
        return f"I study(__) {self.field_of_study} at {self.college_name} and have a masters "


class LinkedInProfile(Profession, Education):
    def __init__(self, headline, industry, job_title: str, company: str, dates_employed: str, college_name: str,
                 degree_name: str, field_of_study: str, secondary_college_name: str,
                 secondary_degree_name: str, secondary_field_of_study: str):
        super().__init__(job_title, company, dates_employed)
        super().__init__(college_name, degree_name, field_of_study, secondary_college_name,
                         secondary_degree_name, secondary_field_of_study)
        self.headline = headline
        self.industry = industry
