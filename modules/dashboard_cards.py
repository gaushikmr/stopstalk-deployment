"""
    Copyright (c) 2015-2020 Raj Patel(raj454raj@gmail.com), StopStalk

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

import utilities
from gluon import current, IMG, DIV, TABLE, THEAD, HR, H5, \
                  TBODY, TR, TH, TD, A, SPAN, INPUT, I, P, \
                  TEXTAREA, SELECT, OPTION, URL, BUTTON, TAG

# ==============================================================================
class BaseCard:
    # --------------------------------------------------------------------------
    def __init__(self, user_id, card_type):
        self.user_id = user_id
        self.card_type = card_type

    # --------------------------------------------------------------------------
    def get_html(self, **args):
        if self.card_type == "simple_with_cta":
            return DIV(DIV(DIV(SPAN(args["card_title"], _class="card-title"),
                               P(args["card_text"]),
                                _class="card-content " + \
                                       args["card_text_color_class"]),
                           DIV(A(args["card_action_text"],
                                 _href=args["card_action_url"],
                                 _class="btn btn-default",
                                 _target="_blank"),
                               _class="card-action right-text"),
                           _class="card " + args["card_color_class"]),
                       _class="col s4")
        elif self.card_type == "simple_with_multiple_ctas":
            return DIV(DIV(DIV(SPAN(args["card_title"], _class="card-title"),
                               P(args["card_text"]),
                                _class="card-content " + \
                                       args["card_text_color_class"]
                               ),
                           DIV(*args["cta_links"],
                               _class="card-action"),
                           _class="card " + args["card_color_class"]),
                       _class="col s4")
        elif self.card_type == "with_html":
            return DIV(DIV(DIV(SPAN(args["card_title"], _class="card-title"),
                               args["custom_html"],
                                _class="card-content " + \
                                       args["card_text_color_class"]),
                           DIV(A(args["card_action_text"],
                                 _href=args["card_action_url"],
                                 _class="btn btn-default",
                                 _target="_blank"),
                               _class="card-action right-text"),
                           _class="card " + args["card_color_class"]),
                       _class="col s4")

    # --------------------------------------------------------------------------
    def get_data(self):
        pass

# ==============================================================================
class StreakCard(BaseCard):
    # --------------------------------------------------------------------------
    def __init__(self, user_id, kind):
        self.genre = StreakCard.__name__
        self.kind = kind
        self.key_name = "curr_%s_streak" % self.kind
        self.user_id = user_id
        self.card_title = "Keep your %s streak going!" % self.kind
        self.stats = None
        BaseCard.__init__(self, user_id, "simple_with_cta")

    # --------------------------------------------------------------------------
    def get_html(self):
        streak_value = self.get_data()
        if self.kind == "day":
            card_text = "You're at a %d day streak. Keep solving a new problem everyday!" % streak_value
            card_action_text = "Pick a Problem"
        elif self.kind == "accepted":
            card_text = "You're at a %d accepted problem streak. Let the greens rain!" % streak_value
            card_action_text = "Pick a Problem"
        else:
            return "FAILURE"

        card_action_url = URL("default",
                              "cta_handler",
                              vars=dict(kind="random"))

        card_html = BaseCard.get_html(self, **dict(
                       card_title=self.card_title,
                       card_text=card_text,
                       card_action_text=card_action_text,
                       card_action_url=card_action_url,
                       card_color_class="white",
                       card_text_color_class="black-text"
                    ))
        return card_html

    # --------------------------------------------------------------------------
    def get_data(self):
        if self.stats is None:
            self.stats = utilities.get_rating_information(self.user_id, False)
        return self.stats[self.key_name]

    # --------------------------------------------------------------------------
    def should_show(self):
        return True
        self.stats = utilities.get_rating_information(self.user_id, False)
        return self.stats[self.key_name] > 0

# ==============================================================================
class SuggestProblemCard(BaseCard):
    # --------------------------------------------------------------------------
    def __init__(self, user_id):
        self.genre = SuggestProblemCard.__name__
        self.user_id = user_id
        self.card_title = "Mood"
        BaseCard.__init__(self, self.user_id, "simple_with_multiple_ctas")

    # --------------------------------------------------------------------------
    def get_html(self):
        streak_value = self.get_data()
        card_text = "Let's find you some problem that you can start solving."
        card_action_url = URL("default",
                              "cta_handler",
                              vars=dict(kind="random"))

        card_html = BaseCard.get_html(self, **dict(
                       card_title=self.card_title,
                       card_text=card_text,
                       card_action_text="abcd",
                       cta_links=[
                            A("Easy",
                              _href=URL("default", "cta_handler",
                                        vars=dict(kind="suggested_tag",
                                                  tag_category="Easy")),
                              _class="btn btn-default",
                              _target="_blank"),
                            " ",
                            A("Medium",
                              _href=URL("default", "cta_handler",
                                        vars=dict(kind="suggested_tag",
                                                  tag_category="Medium")),
                              _class="btn btn-default",
                              _target="_blank"),
                            " ",
                            A("Hard",
                              _href=URL("default", "cta_handler",
                                        vars=dict(kind="suggested_tag",
                                                  tag_category="Hard")),
                              _class="btn btn-default",
                              _target="_blank"),
                       ],
                       card_color_class="white",
                       card_text_color_class="black-text"
                    ))
        return card_html

    # --------------------------------------------------------------------------
    def get_data(self):
        pass

    # --------------------------------------------------------------------------
    def should_show(self):
        return True

# ==============================================================================
class UpcomingContestCard(BaseCard):

    # --------------------------------------------------------------------------
    def __init__(self, user_id):
        self.genre = UpcomingContestCard.__name__
        self.user_id = user_id
        self.card_title = "Upcoming contests"
        BaseCard.__init__(self, self.user_id, "with_html")

    # --------------------------------------------------------------------------
    def get_html(self):
        contest_data = self.get_data()
        card_content_table = TABLE(
            _class="bordered centered highlight",
            _style="line-height: 20px"
        )
        tbody = TBODY()

        for contest in contest_data:
            tbody.append(TR(TD(contest[0]),
                            TD(IMG(_src=current.get_static_url(
                                            "images/%s_small.png" % contest[1]
                                        ),
                                   _style="height: 30px; width: 30px;")),
                            TD(A(I(_class="fa fa-external-link-square"),
                                 _class="btn-floating btn-small accent-4 green view-contest",
                                 _href=contest[2],
                                 _target="_blank"))))

        card_content_table.append(tbody)

        card_action_url = URL("default",
                              "cta_handler",
                              vars=dict(kind="random"))

        card_html = BaseCard.get_html(self, **dict(
                       card_title=self.card_title,
                       custom_html=card_content_table,
                       card_action_text="View all",
                       card_action_url=URL("default", "contests"),
                       card_color_class="white",
                       card_text_color_class="black-text"
                    ))
        return card_html

    # --------------------------------------------------------------------------
    def get_data(self):
        _, upcoming = utilities.get_contests()
        data = []
        for contest in upcoming[:2]:
            data.append((
                contest["Name"],
                str(contest["Platform"]).lower(),
                contest["url"]
            ))
        return data

    # --------------------------------------------------------------------------
    def should_show(self):
        return True

# ==============================================================================
class RecentSubmissionsCard(BaseCard):
    # --------------------------------------------------------------------------
    def __init__(self, user_id):
        self.genre = RecentSubmissionsCard.__name__
        self.user_id = user_id
        self.card_title = "Recent Friends' submissions"
        self.final_data = None
        BaseCard.__init__(self, user_id, "with_html")

    # --------------------------------------------------------------------------
    def get_html(self):
        submissions_data = self.get_data()
        card_action_url = URL("default",
                              "submissions",
                              args=[1])

        card_content_table = TABLE(
            _class="bordered highlight"
        )
        tbody = TBODY()

        for row in submissions_data:
            user_record = utilities.get_user_records([row[0]], "id", "id", True)
            tr = TR(TD(A(user_record.first_name + " " + user_record.last_name,
                                 _href=URL("user", "profile",
                                           args=user_record.stopstalk_handle,
                                           extension=False),
                                 _target="_blank")))

            td = TD()
            for site in row[1]:
                if site == "total":
                    continue
                else:
                    td.append(SPAN(IMG(_src=current.get_static_url(
                                                "images/%s_small.png" % str(site).lower()
                                            ),
                                       _style="height: 18px; width: 18px; margin-bottom: -4px;"),
                                   " " + str(row[1][site]),
                                   _style="padding-right: 10px;"))
            tr.append(td)
            tbody.append(tr)

        card_content_table.append(tbody)

        card_html = BaseCard.get_html(self, **dict(
                       card_title=self.card_title,
                       custom_html=card_content_table,
                       card_action_text="View all",
                       card_action_url=card_action_url,
                       card_color_class="white",
                       card_text_color_class="black-text"
                    ))
        return card_html

    # --------------------------------------------------------------------------
    def get_data(self):
        return self.final_data if self.final_data is not None else "FAILURE"

    # --------------------------------------------------------------------------
    def should_show(self):
        import datetime
        db = current.db
        stable = db.submission
        friends, _ = utilities.get_friends(self.user_id)
        today = datetime.datetime.today()
        last_week = today - datetime.timedelta(days=150)
        rows = db.executesql("""
            SELECT user_id, site, count(*)
            FROM submission
            WHERE time_stamp >= "%s" AND
                user_id in (%s) AND custom_user_id is NULL
            GROUP BY 1, 2
            ORDER BY 3 DESC
        """ % (str(last_week.date()),
               ",".join([str(x) for x in friends])))
        final_hash = {}
        for row in rows:
            if row[0] not in final_hash:
                final_hash[row[0]] = {"total": 0}
            final_hash[row[0]][row[1]] = row[2]
            final_hash[row[0]]["total"] += row[2]

        final_data = sorted(final_hash.items(),
                            key=lambda x: x[1]["total"],
                            reverse=True)[:2]
        if len(final_data) > 0:
            self.final_data = final_data
            return True
        return False

# ==============================================================================