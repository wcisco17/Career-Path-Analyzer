from time import sleep
from typing import List

from parsel import Selector
from prompts import position


def get_helper(html, clas, clas_nester, is_experience: bool) -> [str]:
    selector_helper = Selector(html)
    selector_class = selector_helper.xpath(
        f"//div[@id='{clas}']/following-sibling::div/following-sibling::div"
    ).getall()
    new_arr = []
    more_experience = []
    if selector_class:
        for val in selector_class:
            selection_sel = Selector(val)
            deep_nester = selection_sel.xpath(
                f"//li[@class='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column']"
            ).getall()

            new_arr = ["" for _ in range(len(deep_nester) + 1)]

            if deep_nester:
                for i, li_items in enumerate(deep_nester):
                    selection_li_items = Selector(li_items)
                    list_item = selection_li_items.xpath(f"//{str(clas_nester)}//text()")
                    selection_more_experience = selection_li_items.xpath(
                        f"//div[@class='pvs-list__outer-container']/ul/li/span[@class='pvs-entity__path-node']" +
                        f"/following-sibling::div"
                    )

                    if len(selection_more_experience) > 1:
                        selection_header_experience = selection_li_items.xpath(
                            f"//div[@class='display-flex flex-column full-width align-self-center']" +
                            f"/div[@class='display-flex flex-row justify-space-between']" +
                            f"/a[@data-field='experience_company_logo']//text()"
                        ).getall()
                        experience_header = clean_values(selection_header_experience)
                        experience_header = remove_duplicate(experience_header)

                        more_experience = ["" for _ in range(len(selection_more_experience) + 1)]

                        for j, experience in enumerate(selection_more_experience.getall()):
                            item = Selector(experience)
                            list_experience = item.xpath('//div//text()')
                            more_experience[j] = ['more-experience'] + experience_header + list_experience.getall()
                            more_experience = [clean_values(value) for value in more_experience]
                            more_experience = [remove_duplicate(value) for value in more_experience]
                    else:
                        if is_experience:
                            new_arr[i] = ['experience'] + list_item.getall()
                        else:
                            new_arr[i] = list_item.getall()
                        new_arr = [clean_values(value) for value in new_arr]
                        new_arr = [remove_duplicate(value) for value in new_arr]
    return new_arr, more_experience


def remove_duplicate(data) -> [str]:
    dup = {}
    for deep_item in data:
        if deep_item not in dup:
            dup[deep_item] = True
    return list(dup.keys())


def clean_values(cc) -> [str]:
    item = []
    for vl in cc:
        vl = vl.replace('\n', '').strip()
        vl = vl.replace('\t', '').strip()
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
        '//*[starts-with(@class, "pv-text-details__left-panel")]').get()
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
        clas="experience",
        clas_nester="li",
        is_experience=True
    )
    return experience


# Education


def get_education_list(html):
    education = get_helper(
        html=html,
        clas="education",
        clas_nester="li",
        is_experience=False
    )
    return education


#  Many positions (Nested)


def get_many_experiences(html):
    many_positions = get_helper(
        html=html,
        clas="artdeco-card ember-view break-words pb3 mt2",
        clas_nester="li",
        is_experience=False
    )
    return many_positions


def get_skills(html) -> str:
    skill = get_helper(
        html=html,
        clas="skills",
        clas_nester="li",
        is_experience=False
    )
    list_of_skills = [item for item in skill]
    c = ''
    if len(list_of_skills) > 1:
        for deep in skill:
            if len(deep) > 1:
                for deeper in deep:
                    if len(deeper) > 1:
                        c += deeper[0] + ','

    return c
