import json
import click
import requests
from lxml import html

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.122 Safari/537.36 '
}

data = {
    'form_rcdl': 'form_rcdl',
    'javax.faces.source': 'form_rcdl:j_idt34:CaptchaID',
    'javax.faces.partial.event': 'blur',
    'javax.faces.partial.execute': 'form_rcdl:j_idt34:CaptchaID',
    'javax.faces.partial.render': 'form_rcdl:j_idt34:CaptchaID',
    'CLIENT_BEHAVIOR_RENDERING_MODE': 'OBSTRUSIVE',
    'javax.faces.behavior.event': 'blur',
    'javax.faces.partial.ajax': 'true'
}

data_dict = {
    'current_status': '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[1]/td[2]/span/text()',
    'holders_name': '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[2]/td[2]/text()',
    'date_of_issue': '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[3]/td[2]/text()',
    'last_transaction_at': '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[4]/td[2]/text()',
    'driving_licence_no': '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[5]/td[2]/text()',
    'non_transport_valid_from': '//*[@id="form_rcdl:j_idt118"]/table[2]/tbody/tr[1]/td[2]/text()',
    'non_transport_valid_to': '//*[@id="form_rcdl:j_idt118"]/table[2]/tbody/tr[1]/td[3]/text()',
    'transport_valid_from': '//*[@id="form_rcdl:j_idt118"]/table[2]/tbody/tr[2]/td[2]/text()',
    'transport_valid_to': '//*[@id="form_rcdl:j_idt118"]/table[2]/tbody/tr[2]/td[3]/text()',
    'hazardous_valid_till': '//*[@id="form_rcdl:j_idt118"]/table[3]/tbody/tr/td[2]/text()',
    'hill_valid_till': '//*[@id="form_rcdl:j_idt118"]/table[3]/tbody/tr/td[4]/text()',
    'class_of_veh_category': '//*[@id="form_rcdl:j_idt167_data"]/tr/td[1]/text()',
    'class_of_veh': '//*[@id="form_rcdl:j_idt167_data"]/tr/td[2]/text()',
    'class_of_veh_issue_date': '//*[@id="form_rcdl:j_idt167_data"]/tr/td[3]/text()',
}


def get_captcha(source_code):  # pass the required params and return the decoded string
    path = '//*[@id="form_rcdl:j_idt34:j_idt41"]/@src'  # the xpath to the src attr. of the captcha image
    return ""


@click.command()
def main():
    licence = click.prompt("enter your driving licence number format('SS-RRYYYYNNNNNNN')")
    dob = click.prompt("enter your date of birth format('dd-mm-yyyy')")

    with requests.session() as s:
        tries = 0
        while tries < 3:
            click.echo(f"try number {tries + 1}")
            url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
            r = s.get(url, headers=headers, timeout=5)
            byte_data = r.content
            source_code = html.fromstring(byte_data)

            p1 = '//input[@name="javax.faces.ViewState"]/@value'
            x = source_code.xpath(p1)
            data['javax.faces.ViewState'] = x[0]
            data['form_rcdl:tf_dlNO'] = licence
            data['form_rcdl:tf_dob_input'] = dob
            data['form_rcdl:j_idt34:CaptchaID'] = get_captcha(source_code)
            r = s.post(url, data=data, headers=headers)

            byte_data = r.content
            source_code = html.fromstring(byte_data)

            try:
                success = '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[5]/td[2]/text()'
                x = source_code.xpath(success)
                if x[0] == licence:
                    click.echo("authentication was successful")
            except:
                click.echo("authentication failed")
                tries += 1
                continue

            results = {}

            for k, v in data_dict.items():
                tree = source_code.xpath(v)
                results[k] = tree[0]

            results = json.dumps(results)
            loaded_results = json.loads(results)
            click.echo(loaded_results)


if __name__ == '__main__':
    main()
