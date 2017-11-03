command: "~/Projects/isbw-cli-widget/env/bin/python ~/Projects/isbw-cli-widget/isbw.py --html"

# refresh every hour
refreshFrequency: "1h"

# render gets called after the shell command has executed. The command's output
# is passed in as a string. Whatever it returns will get rendered as HTML.
render: (output) -> """
  <h1>I Should Be Writing</h1>
  #{output}
"""

# the CSS style for this widget, written using Stylus
# (http://learnboost.github.io/stylus/)
style: """
  background: rgba(#fff, 0.6)
  border-radius: 20px
  color: #141f33
  font-family: Helvetica Neue
  font-weight: 400
  line-height: 1.5
  padding: 20px
  top: 3%
  left: 2%

  h1
    font-size: 30px
    font-weight: 700
    margin: 0px
    text-decoration: underline
    line-height: 1.0
    margin-top: 5px
    margin-bottom: 10px
    text-align: center

  table
    text-align: center
  td.label
    padding-left: 40px
    text-align: left
  tr.total td
    padding-top: 10px
    font-weight: 600
"""
