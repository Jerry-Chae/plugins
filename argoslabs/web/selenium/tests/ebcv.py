"""
====================================
 :mod:`ebcv`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: eVOLCANO License

Description
===========
eVOLCANO English Brain Craft Video : Youtube Channel Crawler
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/07/11]
#     - add YoutubeVideo
#  * [2021/07/08]
#     - starting

################################################################################
import os
import sys
import csv
import shutil
import requests
import datetime
import traceback
from alabs.common.util.vvlogger import get_logger
from alabs.selenium import PySelenium
from tempfile import gettempdir


################################################################################
class YoutubeVideo(PySelenium):
    HEADER = (
        'channel_id',
        'video_id',
        'url',
        'title',
        'label',
        'have_script',
    )
    # languages: Korean, Thai, Indonesian, Simplified Chinese, Vietnamese, ...
    SUB_LANGS = {
        # 'Afrikaans': 'af',
        # 'Arabic': 'ar',
        # 'Bengali': 'bn',
        # 'Bosnian': 'bs',
        # 'Catalan': 'ca',
        # 'Czech': 'cs',
        # 'Welsh': 'cy',
        # 'Danish': 'da',
        # 'German': 'de',
        # 'Greek': 'el',
        'English': 'en',
        # 'Esperanto': 'eo',
        # 'Spanish': 'es',
        # 'Estonian': 'et',
        # 'Finnish': 'fi',
        # 'French': 'fr',
        # 'Hindi': 'hi',
        # 'Croatian': 'hr',
        # 'Hungarian': 'hu',
        # 'Armenian': 'hy',
        'Indonesian': 'id',
        # 'Icelandic': 'is',
        # 'Italian': 'it',
        # 'Japanese': 'ja',
        # 'Javanese': 'jw',
        # 'Khmer': 'km',
        'Korean': 'ko',
        # 'Latin': 'la',
        # 'Latvian': 'lv',
        # 'Macedonian': 'mk',
        # 'Malayalam': 'ml',
        'Malay': 'ms',
        # 'Marathi': 'mr',
        # 'Myanmar (Burmese)': 'my',
        # 'Nepali': 'ne',
        # 'Dutch': 'nl',
        # 'Norwegian': 'no',
        # 'Polish': 'pl',
        # 'Portuguese': 'pt',
        # 'Romanian': 'ro',
        # 'Russian': 'ru',
        # 'Sinhala': 'si',
        # 'Slovak': 'sk',
        # 'Albanian': 'sq',
        # 'Serbian': 'sr',
        # 'Sundanese': 'su',
        # 'Swedish': 'sv',
        # 'Swahili': 'sw',
        # 'Tamil': 'ta',
        # 'Telugu': 'te',
        'Thai': 'th',
        'Filipino': 'tl',
        # 'Turkish': 'tr',
        # 'Ukrainian': 'uk',
        'Vietnamese': 'vi',
        'Chinese': 'zh',
    }

    # ==========================================================================
    # noinspection PyDefaultArgument
    def __init__(self,
                 out_folder,
                 channel_id,
                 max_videos=100,
                 **kwargs):
        kwargs['url'] = 'https://www.youtube.com/channel/' + channel_id
        out_folder = os.path.join(out_folder, channel_id)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
        self.out_folder = out_folder
        self.channel_id = channel_id
        self.max_videos = max_videos
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting eVOLCANO Youtube Videos for channel "{channel_id}"...')
        csv_f = os.path.join(self.out_folder, 'videos.csv')
        self.logger.info(f'Videos CSV is "{csv_f}"')
        # for output
        self.cwf = open(csv_f, 'w', encoding='utf-8')
        self.cw = csv.writer(self.cwf, lineterminator='\n')
        self.rows = list()
        self.cw.writerow(self.HEADER)
        self.ids = {}

    # ==========================================================================
    def close(self):
        self.cwf.close()
        PySelenium.close(self)

    # ==========================================================================
    def get_script(self, video_id, sub_lang='en', timeout=5):
        url = f'http://video.google.com/timedtext?lang={sub_lang}&v={video_id}'

        script_t = os.path.join(gettempdir(), 'EngBrainCraftVideo.xml')
        try:
            r = requests.get(url, stream=True, timeout=timeout)
            if r.status_code // 10 == 20:
                with open(script_t, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                if os.path.getsize(script_t) <= 0:
                    os.remove(script_t)
                    return False
                script_f = os.path.join(self.out_folder, sub_lang, f'{video_id}.xml')
                if not os.path.exists(os.path.dirname(script_f)):
                    os.makedirs(os.path.dirname(script_f))
                shutil.move(script_t, script_f)
                return True
            return False
        except requests.Timeout:
            self.logger.debug(f'<{video_id}>: sub_lang="{sub_lang}" timeout')
            return False

    # ==========================================================================
    def do_search(self):
        try:
            # Movie Tab
            e = self.get_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[2]',
                                  cond='element_to_be_clickable',
                                  move_to_element=True)
            self.safe_click(e)
            self.implicitly_wait(after_wait=1)

            # Results Div
            divs = self.get_by_xpath('//*[@id="items"]')
            # its = divs.find_elements_by_xpath(".//ytd-grid-video-renderer")
            for i in range(self.max_videos):
                it = self.get_by_xpath(f'//*[@id="items"]/ytd-grid-video-renderer[{i+1}]',
                                       move_to_element=True)
                a = it.find_element_by_xpath('.//*[@id="video-title"]')
                label = a.get_attribute('aria-label')
                title = a.get_attribute('title')
                url = 'https://www.youtube.com' + a.get_attribute('href')
                video_id = url.split('?v=')[-1]
                if video_id in self.ids:
                    raise ReferenceError(f'Duplicate video "{video_id}"')

                num_subtitles = 0
                for lang, lang_code in self.SUB_LANGS.items():
                    have_script = self.get_script(video_id, sub_lang=lang_code)
                    self.logger.debug(f'<{video_id}>: Has {lang} subtitle? {have_script}')
                    if have_script:
                        num_subtitles += 1
                if num_subtitles > 0:
                    row = (self.channel_id, video_id, url, title, label)
                    self.logger.debug(f'<{video_id}>: title="{title}"')
                    self.cw.writerow(row)
                else:
                    self.logger.debug(f'<{video_id}>: has no subtitle')
                self.ids[video_id] = title

        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('do_search Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        self.do_search()


################################################################################
def do_yv_start(outf, channel_id, **kwargs):
    with YoutubeVideo(outf, channel_id, **kwargs) as ws:
        ws.start()



################################################################################
class EngBrainCraftVideo(PySelenium):
    MAIN_HEADER = (
        'channel_id',
        'subscribers',
        'videos',
        'total_views',
        'latest_video',
        'channel_url',
        'title',
    )

    # ==========================================================================
    # noinspection PyDefaultArgument
    def __init__(self,
                 out_folder,
                 channel_name=None,
                 category=['Education'],
                 topics=None,
                 languages=['English'],
                 countries=['United States', 'United Kingdom'],
                 create_date=None,
                 subscribers=None,
                 total_views=None,
                 total_videos=None,
                 latest_videos=None,
                 keywords=None,
                 sort_by='Subscribers (descending)',
                 max_page=10,
                 **kwargs):
        kwargs['url'] = 'https://www.channelcrawler.com/'
        self.out_folder = out_folder
        self.channel_name = channel_name
        self.category = category
        self.topics = topics
        self.languages = languages
        self.countries = countries
        self.create_date = create_date
        self.subscribers = subscribers
        self.total_views = total_views
        self.total_videos = total_videos
        self.latest_videos = latest_videos
        self.keywords = keywords
        self.sort_by = sort_by
        self.max_page = max_page
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting eVOLCANO Youtube channel crawler ...')
        self.main_csv = os.path.join(self.out_folder, 'main.csv')
        self.logger.info(f'main CSV is "{self.main_csv}"')
        # for output
        self.cwf = open(self.main_csv, 'w', encoding='utf-8')
        self.cw = csv.writer(self.cwf, lineterminator='\n')
        self.rows = list()
        self.cw.writerow(self.MAIN_HEADER)
        self.ids = {}

    # ==========================================================================
    def close(self):
        self.cwf.close()
        PySelenium.close(self)

    # ==========================================================================
    def do_page(self, page_num):
        self.logger.info(f'Get Items from page {page_num}')
        page = self.get_by_xpath('//*[@id="main-content"]/div[2]')
        its = page.find_elements_by_xpath(".//div")
        for i, it in enumerate(its):
            row = list()
            tag = it.find_element_by_xpath(".//h4/a")
            href = tag.get_attribute('href')
            channel_id = href.split('/')[-1]
            if channel_id in self.ids:
                raise IndexError(f'End of Result or duplicate id {channel_id}')
            row.append(channel_id)
            tags = it.find_elements_by_xpath(".//a")
            title = tags[1].get_attribute('title').replace('\n', ' ')
            tags = it.find_elements_by_xpath(".//small")
            content = tags[1].text.split('\n')
            # 115M Subscribers
            row.append(content[0].split()[0])
            # 662 Videos
            row.append(content[1].split()[0])
            # 1.5B Total Views
            row.append(content[2].split()[0])
            # Latest Video: Jul 08 2021
            datestr = ' '.join(content[3].split()[2:])
            dt = datetime.datetime.strptime(datestr, "%b %d %Y").date()
            row.append(dt.strftime("%Y-%m-%d"))
            row.append(href)
            row.append(title)
            self.logger.debug(f'[{page_num}][{i+1}] item: {row[:-2]}')
            self.cw.writerow(row)
            self.ids[channel_id] = (page_num, i+1)

    # ==========================================================================
    def do_search(self):
        try:
            # Channel Name
            if self.channel_name:
                self.logger.info(f'Criteria channel_name: {self.channel_name}')
                e = self.get_by_xpath('//*[@id="queryName"]')
                e.send_keys(self.channel_name)

            # Category
            if self.category:
                self.logger.info(f'Criteria category: {self.category}')
                # click Category "dropdown-display-label
                e = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[2]/div/div/div[1]',
                                      cond='element_to_be_clickable', move_to_element=True)
                self.safe_click(e)
                self.implicitly_wait(after_wait=1)

                ul = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[2]/div/div/div[2]/ul')
                lis = ul.find_elements_by_xpath(".//*")
                for li in lis:
                    b_found = False
                    for category in self.category:
                        if li.text.strip().lower() == category.strip().lower():
                            b_found = True
                            break
                    if b_found:
                        li.click()
                # unshow dropdown selection
                e = self.get_by_xpath('/html/body/div/div[3]/div/div[1]')
                self.safe_click(e)

            # Topics
            if self.topics:
                self.logger.info(f'Criteria topics: {self.topics}')
                # click Category "dropdown-display-label
                e = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[3]/div/div/div[1]',
                                      cond='element_to_be_clickable', move_to_element=True)
                self.safe_click(e)
                self.implicitly_wait(after_wait=1)

                ul = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[3]/div/div/div[2]/ul')
                lis = ul.find_elements_by_xpath(".//*")
                for li in lis:
                    b_found = False
                    for topics in self.topics:
                        if li.text.strip().lower() == topics.strip().lower():
                            b_found = True
                            break
                    if b_found:
                        li.click()
                # unshow dropdown selection
                e = self.get_by_xpath('/html/body/div/div[3]/div/div[1]')
                self.safe_click(e)

            # Languages
            if self.languages:
                self.logger.info(f'Criteria languages: {self.languages}')
                # click Category "dropdown-display-label
                e = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[4]/div/div/div[1]',
                                      cond='element_to_be_clickable', move_to_element=True)
                self.safe_click(e)
                self.implicitly_wait(after_wait=1)

                ul = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[4]/div/div/div[2]/ul')
                lis = ul.find_elements_by_xpath(".//*")
                for li in lis:
                    b_found = False
                    # Skip English because of default and Toggle
                    if li.text.strip().lower() == 'english':
                        continue
                    for languages in self.languages:
                        if li.text.strip().lower() == languages.strip().lower():
                            b_found = True
                            break
                    if b_found:
                        li.click()
                # unshow dropdown selection
                e = self.get_by_xpath('/html/body/div/div[3]/div/div[1]')
                self.safe_click(e)

            # Countries
            if self.countries:
                self.logger.info(f'Criteria countries: {self.countries}')
                # click Category "dropdown-display-label
                e = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[5]/div/div/div[1]',
                                      cond='element_to_be_clickable', move_to_element=True)
                self.safe_click(e)
                self.implicitly_wait(after_wait=1)

                ul = self.get_by_xpath('//*[@id="queryIndexForm"]/div[2]/div[1]/div[5]/div/div/div[2]/ul')
                lis = ul.find_elements_by_xpath(".//*")
                for li in lis:
                    b_found = False
                    for countries in self.countries:
                        if li.text.strip().lower() == countries.strip().lower():
                            b_found = True
                            break
                    if b_found:
                        li.click()
                # unshow dropdown selection
                e = self.get_by_xpath('/html/body/div/div[3]/div/div[1]')
                self.safe_click(e)

            # Keywords
            if self.keywords:
                self.logger.info(f'Criteria keywords: {self.keywords}')
                e = self.get_by_xpath('//*[@id="queryDescription"]')
                e.send_keys(self.keywords)


            # Submit button
            e = self.get_by_xpath('/html/body/div/div[3]/div/div[1]/div[2]/div/button',
                                  cond='element_to_be_clickable',
                                  move_to_element=True)
            self.safe_click(e)
            self.implicitly_wait(after_wait=0.2)

            # Sort By
            if self.sort_by:
                self.select_by_visible_text('//*[@id="sort-select"]', self.sort_by)
                self.implicitly_wait(after_wait=0.3)

            # for pagenation with max_page
            for i in range(self.max_page):
                self.do_page(i+1)
                pagenation = self.get_by_xpath('//*[@id="main-content"]/div[3]/div/nav/ul')
                tag_as = pagenation.find_elements_by_xpath(".//a")
                next_a = tag_as[-1]
                self.safe_click(next_a)
                self.implicitly_wait(after_wait=0.2)

        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('do_search Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        self.do_search()


################################################################################
def do_yc_start(outf, **kwargs):
    with EngBrainCraftVideo(outf, **kwargs) as ws:
        ws.start()
        main_csv = ws.main_csv
    with open(main_csv, encoding='utf-8') as ifp:
        cr = csv.reader(ifp)
        for i, row in enumerate(cr):
            if i < 1:
                continue
            _kwargs = {
                # 'browser': 'Chrome',
                'browser': 'Edge',
                'logger': logger,
                'max_videos': 300,
            }
            channel_id = row[0]
            do_yv_start(outf, channel_id, **_kwargs)


################################################################################
if __name__ == '__main__':
    rootf = r'W:\eVOLCANO\EBCV\work\YCC'
    outf = rf'{rootf}\{datetime.datetime.now().strftime("%Y%m%d")}'
    if not os.path.exists(outf):
        os.makedirs(outf)
    log_f = os.path.join(rootf, "EngBrainCraftVideo.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    _kwargs = {
        # 'browser': 'Chrome',
        'browser': 'Edge',
        'logger': logger,

        # for Criteria
        'channel_name': None,
        # 'channel_name': 'comedy',

        'category': ['Education'],
        # 'category': ['Education', 'Comedy'],

        'topics': None,
        # 'topics': ['Sport', 'Vehicle'],

        'languages': ['English'],
        # 'languages': ['English', 'Korean'],

        'countries': ['United States', 'United Kingdom'],

        'create_date': None,
        'subscribers': None,
        'total_views': None,
        'total_videos': None,
        'latest_videos': None,

        'keywords': None,
        # 'keywords': 'minecraft',
        # 'keywords': '-minecraft',

        'sort_by': 'Subscribers (descending)',
        'max_page': 3,
    }
    do_yc_start(outf, **_kwargs)

