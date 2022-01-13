from time import sleep

from parsel import Selector

from lib.prompts import position


def get_helper(html, clas, clas_nester):
    selector_helper = Selector(html)
    selector_class = selector_helper.xpath(
        f'//*[starts-with(@class, "{str(clas)}")]'
    ).getall()
    new_arr = []
    if selector_class:
        for val in selector_class:
            selection_sel = Selector(val)
            deep_nester = selection_sel.xpath(f"//{str(clas_nester)}//text()")
            sleep(1)
            if deep_nester:
                new_arr.append(deep_nester.getall())
                new_arr = [clean_values(
                    value) for value in new_arr]
    return new_arr


def clean_values(cc):
    item = []
    for vl in (cc):
        vl = vl.replace('\n', '').strip()
        if vl != "":
            item.append(vl)
    return item


# Industry
def get_industry():
    return {"Industry": position}

# Get headline


def get_headline(html):
    selector_headline = Selector(html)
    headline = selector_headline.xpath(
        '//*[starts-with(@class, "artdeco-card ember-view pv-top-card")]').get()
    if headline:
        headline = selector_headline.xpath(
            '//*[starts-with(@class, "text-body-medium break-words")]//text()').get()
        return {"Headline": headline.strip()}
    else:
        return None

# ONLY ONE TYPE OF EXPERIENCE (No more than 1 position)


def get_experience(html):
    experience = get_helper(
        html=html,
        clas="pv-entity__position-group-pager pv-profile-section__list-item ember-view",
        clas_nester="section"
    )
    return experience
# Education


def get_education_list(html):
    education = get_helper(
        html=html,
        clas="pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view",
        clas_nester="li"
    )
    return education

#  Many positions (Nested)


def get_many_experiences(html):
    many_positions = get_helper(
        html=html,
        clas="pv-entity__position-group-role-item",
        clas_nester="li"
    )
    return many_positions


def get_skills(html):
    skill = get_helper(
        html=html,
        clas="pv-skill-category-entity__top-skill pv-skill-category-entity pb3 pt4 pv-skill-endorsedSkill-entity relative ember-view",
        clas_nester="li"
    )
    list_of_skills = [item[0] for item in skill]
    return list_of_skills
