import json
import datetime
import platform
import base64


# Dependency inversion principle: Abstract classes/interfaces
class FileHandler:
    def load_json_file(self, file_path):
        raise NotImplementedError


class ImageHandler:
    def img_to_base64(self, img_path):
        raise NotImplementedError


class ReportGenerator:
    def generate_result_table(self, comparison_file, env_files):
        raise NotImplementedError


class JsonFileHandler(FileHandler):
    def load_json_file(self, file_path):
        with open(file_path, "r") as json_file:
            return json.load(json_file)


class Base64ImageHandler(ImageHandler):
    def img_to_base64(self, img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')


class HTMLReportGenerator(ReportGenerator):
    def __init__(self, file_handler: FileHandler, image_handler: ImageHandler):
        self.file_handler = file_handler
        self.image_handler = image_handler

    def generate_result_table(self, comparison_file, env_files):
        col_head = "<th>Result</th>\n<th>Check_name</th>\n"
        data_main = ""
        i = 1

        # Load comparison data
        comparison_data = self.file_handler.load_json_file(comparison_file)

        # Extract environments from file_paths dict keys, excluding 'comparison'
        environments = [env for env in env_files.keys() if env != 'comparison']

        # Add environment columns dynamically based on environments list
        for env in environments:
            col_head += f"<th>{env.capitalize()}</th>\n"

        for check_item in comparison_data:
            check_name = check_item["Name"]
            data_row1 = (f'<tr class="results-table {check_item["Status"].lower()}" data-toggle="collapse" id="row{i}" '
                         f'data-target=".row{i}" onclick="toggleDetails(\'row{i}\')">\n')
            data_main += data_row1
            data_main += f"<td class='{check_item['Status'].lower()}'>{check_item['Status'].capitalize()}</td>\n"
            data_main += f"<td>{check_name}</td>\n"

            for env in environments:
                env_file = env_files.get(env)
                if env_file:
                    env_details = next((env_item for env_item in env_file if env_item["Name"] == check_name), None)
                    if env_details:
                        data_main += f"<td>{env_details['Status']}</td>\n"
                    else:
                        data_main += "<td></td>\n"
                else:
                    data_main += "<td></td>\n"

            data_row2 = f'</tr><tr class="collapse row{i}" style="display: none;">\n'
            data_main += data_row2
            data_main += f'<td>{check_item["Description"]}</td>\n'
            data_main += f'<td>{check_item["Description"]}</td>\n'

            for env in environments:
                env_file = env_files.get(env)
                if env_file:
                    env_details = next((env_item for env_item in env_file if env_item["Name"] == check_name), None)
                    if env_details:
                        # if env_details["image"]: img_base64 = img_to_base64(env_details["image"]) img_tag = f'<img
                        # src="data:image/png;base64,{img_base64}" alt="{env_details["Name"]}" width="200"
                        # onclick="enlargeImage(this.src)"/>'
                        data_main += f'<td>{env_details["Actual_Result"]}</td>\n'
                    else:
                        data_main += "<td></td>\n"
                else:
                    data_main += "<td></td>\n"

            data_row3 = '<td><input type="checkbox" /> Select</td></tr>\n'
            data_main += data_row3
            i += 1

        return col_head, data_main


def generate_html_report(file_paths, subscription):
    file_handler = JsonFileHandler()
    image_handler = Base64ImageHandler()
    report_generator = HTMLReportGenerator(file_handler, image_handler)

    comparison_file = file_paths['comparison']
    env_files = {env: file_handler.load_json_file(path) for env, path in file_paths.items() if env != 'comparison'}

    env_details = {
        "Site": "Example Site",
        "Subscription": "Paid",
        "Execution Date and Time": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Prod_Url": "http://example.com/prod",
        "Stage_Url": "http://example.com/stage",
        "Dev_Url": "http://example.com/dev",
        "Platform": platform.system(),
        "Total_Execution_Time": "00:10:00",
        "Browser": "Chrome",
        "Browser_ver.": "91.0"
    }

    col_head, data_main = report_generator.generate_result_table(comparison_file, env_files)

    css_styles = '''
    body {
      font-family: Helvetica, Arial, sans-serif;
      font-size: 12px;
      min-width: 800px;
      color: #999;
    }

    h1 {
      font-size: 24px;
      color: black;
    }

    h2 {
      font-size: 16px;
      color: black;
    }

    p {
      color: black;
    }

    a {
      color: #999;
    }

    table {
      border-collapse: collapse;
      width: 100%;
    }

    .metric-card {
      display: inline-block;
      border-radius: 8px;
      padding: 20px;
      margin: 10px;
      text-align: center;
      width: 200px;
      cursor: pointer;
      color: white;
    }

    .metric-card.passed {
      background-color: #4caf50;
    }

    .metric-card.failed {
      background-color: #f44336;
    }

    .metric-card.error {
      background-color: #ff9800;
    }

    .metric-card.existing {
      background-color: #ffeb3b;
      color: black;
    }

    #results-table {
      border: 1px solid #e6e6e6;
      color: #999;
      font-size: 12px;
      width: 100%;
    }

    #results-table th,
    #results-table td {
      padding: 5px;
      border: 1px solid #e6e6e6;
      text-align: left;
    }

    #results-table th {
      font-weight: bold;
    }

    #results-table td.passed {
      color: #4caf50;
    }

    #results-table td.failed {
      color: #f44336;
    }

    #results-table td.existing {
      color: #ffeb3b;
    }

    #results-table td.error {
      color: #ff9800;
    }

    .collapsible:hover {
      cursor: pointer;
      color: #007bff;
    }

    .collapsible {
      color: black;
    }

    .collapsible::after {
      content: " \\25BC";
    }

    .collapsible.expanded::after {
      content: " \\25B2";
    }

    .extras-row.hidden {
      display: none;
    }

    .media-container {
      display: flex;
      align-items: center;
    }

    .media-container img {
      max-width: 100px;
      margin-right: 10px;
    }

    .enlarge-image {
      cursor: pointer;
      max-width: 200px;
      transition: transform 0.2s;
    }

    .enlarge-image:hover {
      transform: scale(1.1);
    }

    .enlarged-image-popup {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 9999;
      background: white;
      border: 2px solid black;
      padding: 10px;
      max-width: 80%;
      max-height: 80%;
      display: none;
    }

    .enlarged-image-popup img {
      width: 100%;
      height: auto;
    }
    '''

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QA Automation Report</title>
        <style>
            {css_styles}
        </style>
        <script>
            function toggleDetails(id) {{
                var elements = document.getElementsByClassName(id);
                for (var i = 0; i < elements.length; i++) {{
                    if (elements[i].style.display === 'none' || elements[i].style.display === '') {{
                        elements[i].style.display = 'table-row';
                    }} else {{
                        elements[i].style.display = 'none';
                    }}
                }}
            }}

            function filterResults(status) {{
                var rows = document.getElementsByClassName('results-table');
                for (var i = 0; i < rows.length; i++) {{
                    if (status === 'all' || rows[i].classList.contains(status)) {{
                        rows[i].style.display = '';
                    }} else {{
                        rows[i].style.display = 'none';
                    }}
                }}
            }}

            function toggleCard(cardClass) {{
                var card = document.querySelector('.' + cardClass);
                if (card.classList.contains('selected')) {{
                    card.classList.remove('selected');
                    filterResults('all');
                }} else {{
                    card.classList.add('selected');
                    filterResults(cardClass);
                }}
            }}

            function enlargeImage(src) {{
                var popup = document.getElementById('enlarged-image-popup');
                var img = popup.querySelector('img');
                img.src = src;
                popup.style.display = 'block';
            }}

            function closeImagePopup() {{
                var popup = document.getElementById('enlarged-image-popup');
                popup.style.display = 'none';
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <h1>QA Automation Report</h1>
            <div id="environment">
                <h2>Environment</h2>
                <table>
                    <tr>
                        <td>
                            <table>
                                <tr><td>Site</td><td>{Site}</td></tr>
                                <tr><td>Subscription</td><td>{Subscription}</td></tr>
                                <tr><td>Prod Url</td><td>{Prod_Url}</td></tr>
                                <tr><td>Stage Url</td><td>{Stage_Url}</td></tr>
                                <tr><td>Dev Url</td><td>{Dev_Url}</td></tr>
                            </table>
                        </td>
                        <td>
                            <table>
                                <tr><td>Environment</td><td>{Platform}</td></tr>
                                <tr><td>Execution Date and Time</td><td>{Execution_Date_and_Time}</td></tr>
                                <tr><td>Total Execution Time</td><td>{Total_Execution_Time}</td></tr>
                                <tr><td>Browser</td><td>{Browser}</td></tr>
                                <tr><td>Browser + ver.</td><td>{Browser_ver}</td></tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="summary">
                <h2>Summary</h2>
                <div class="metric-card passed" onclick="toggleCard('passed')">
                    <h3>Passed</h3>
                    <p>{passed}</p>
                </div>
                <div class="metric-card failed" onclick="toggleCard('failed')">
                    <h3>Failed</h3>
                    <p>{failed}</p>
                </div>
                <div class="metric-card existing" onclick="toggleCard('existing')">
                    <h3>Existing Issues</h3>
                    <p>{xfailed}</p>
                </div>
                <div class="metric-card error" onclick="toggleCard('error')">
                    <h3>Error</h3>
                    <p>{skipped}</p>
                </div>
            </div>
            <div class="results">
                <h2>Results</h2>
                <table id="results-table">
                    <thead id="results-table-head">
                        {col_head}
                    </thead>
                    <tbody>
                        {result_rows}
                    </tbody>
                </table>
            </div>
        </div>
        <div id="enlarged-image-popup" class="enlarged-image-popup" onclick="closeImagePopup()">
            <img src="" alt="Enlarged Image"/>
        </div>
    </body>
    </html>
    '''

    html_content = html_template.format(
        css_styles=css_styles,
        Site=env_details["Site"],
        Subscription=env_details["Subscription"],
        Execution_Date_and_Time=env_details["Execution Date and Time"],
        Prod_Url=env_details["Prod_Url"],
        Stage_Url=env_details["Stage_Url"],
        Dev_Url=env_details["Dev_Url"],
        Platform=env_details["Platform"],
        Total_Execution_Time=env_details["Total_Execution_Time"],
        Browser=env_details["Browser"],
        Browser_ver=env_details["Browser_ver."],
        passed="1",
        failed="2",
        xfailed="3",
        skipped="4",
        col_head=col_head,
        result_rows=data_main
    )

    # Write the HTML content to a file
    with open(f'{subscription}.html', 'w') as f:
        f.write(html_content)

    print("Report generated successfully!")
