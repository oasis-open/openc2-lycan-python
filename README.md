# Lycan
![Supported languages](https://img.shields.io/badge/python-2.7%2C%203.6-blue.svg)
[![Build Status](https://travis-ci.org/oasis-open/openc2-lycan-python.svg)](https://travis-ci.org/open-oasis/openc2-lycan-python)
[![Coverage Status](https://coveralls.io/repos/github/oasis-open/openc2-lycan-python/badge.svg)](https://coveralls.io/github/oasis-open/openc2-lycan-python)

Lycan is an implementation of the OpenC2 OASIS standard for command and control messaging. The current implementation is based on the Language Specification v1.0.

Given the influence of STIX/CyBoX on OpenC2, this library extends the [STIX 2 Python API](https://github.com/oasis-open/cti-python-stix2) internals. Property validation and object extension support aligns with STIX2 conventions.

## Installation

Install with [pip](https://pip.pypa.io/en/stable):

```bash
$ pip install openc2
```

## Usage

```python
import iptc
from openc2 import parse, IPv4Address, Command, Response, Args

# encode
cmd = Command(action = "deny",
              target = IPv4Address(ipv4_net = "1.2.3.4"),
              args = Args(response_requested = "complete"))
msg = cmd.serialize()

# decode
cmd = parse(msg)
if cmd.action == "deny" and cmd.target.type == "ipv4_net":
    rule = iptc.Rule()
    rule.create_match(cmd.target.ipv4_net)
    rule.create_target("DROP")

    if cmd.args.response_requested == 'complete':
        resp = Response(status=200)
        msg = resp.serialize()

# custom actuator
from openc2 import CustomActuator
from stix2 import properties
@CustomActuator('x-acme-widget', [
    ('name', properties.StringProperty(required=True)),
    ('version', properties.FloatProperty())
])
class AcmeWidgetActuator(object):
    def __init__(self, version=None, **kwargs):
        if version and version < 1.0:
            raise ValueError("'%f' is not a supported version." % version)

widget = AcmeWidgetActuator(name="foo", version=1.1)
```

<div>
<h2><a id="readme-general">OASIS TC Open Repository: openc2-lycan-python</a></h2>

<p>This GitHub public repository ( <b><a href="https://github.com/oasis-open/openc2-lycan-python">https://github.com/oasis-open/openc2-lycan-python</a></b> ) was created at the request of the <a href="https://www.oasis-open.org/committees/openc2/">OASIS Open Command and Control (OpenC2) TC</a> as an <a href="https://www.oasis-open.org/resources/open-repositories/">OASIS TC Open Repository</a> to support development of open source resources related to Technical Committee work.</p>

<p>While this TC Open Repository remains associated with the sponsor TC, its development priorities, leadership, intellectual property terms, participation rules, and other matters of governance are <a href="https://github.com/oasis-open/openc2-lycan-python/blob/master/CONTRIBUTING.md#governance-distinct-from-oasis-tc-process">separate and distinct</a> from the OASIS TC Process and related policies.</p>

<p>All contributions made to this TC Open Repository are subject to open source license terms expressed in the <a href="https://www.oasis-open.org/sites/www.oasis-open.org/files/MIT-License.txt">MIT License</a>.  That license was selected as the declared <a href="https://www.oasis-open.org/resources/open-repositories/licenses">"Applicable License"</a> when the TC Open Repository was created.</p>

<p>As documented in <a href="https://github.com/oasis-open/openc2-lycan-python/blob/master/CONTRIBUTING.md#public-participation-invited">"Public Participation Invited</a>", contributions to this OASIS TC Open Repository are invited from all parties, whether affiliated with OASIS or not.  Participants must have a GitHub account, but no fees or OASIS membership obligations are required.  Participation is expected to be consistent with the <a href="https://www.oasis-open.org/policies-guidelines/open-repositories">OASIS TC Open Repository Guidelines and Procedures</a>, the open source <a href="https://github.com/oasis-open/openc2-lycan-python/blob/master/LICENSE">LICENSE</a> designated for this particular repository, and the requirement for an <a href="https://www.oasis-open.org/resources/open-repositories/cla/individual-cla">Individual Contributor License Agreement</a> that governs intellectual property.</p>

</div>

<div>
<h2><a id="purposeStatement">Statement of Purpose</a></h2>

<p>Statement of Purpose for this OASIS TC Open Repository (openc2-lycan-python) as <a href="https://lists.oasis-open.org/archives/openc2/201802/msg00006.html">proposed</a> and <a href="https://lists.oasis-open.org/archives/openc2/201803/msg00007.html">approved</a> [<a href="https://lists.oasis-open.org/archives/openc2/201803/msg00023.html">bis</a>] by the TC:</p>

<p>The purpose of this OASIS TC Open repository is to develop and maintain a python implementation of <a href="http://docs.oasis-open.org/openc2/">OpenC2</a>, and to provide a python codebase to facilitate other prototype efforts.  The python library is designed to support transformations between data-interchange formats (such as JSON) and python language objects.</p>

<p>The OASIS OpenC2 Technical Committee was <a href="https://www.oasis-open.org/committees/openc2/charter.php">chartered</a> to address matters as they pertain to command and control of cyber defense technologies, and to maintain a library of prototype implementations.</p>

</div>

<div><h2><a id="purposeClarifications">Additions to Statement of Purpose</a></h2>

<p>Repository Maintainers may include here any clarifications &mdash; any additional sections, subsections, and paragraphs that the Maintainer(s) wish to add as descriptive text, reflecting (sub-) project status, milestones, releases, modifications to statement of purpose, etc.  The project Maintainers will create and maintain this content on behalf of the participants.</p>
</div>

<div>
<h2><a id="maintainers">Maintainers</a></h2>

<p>TC Open Repository <a href="https://www.oasis-open.org/resources/open-repositories/maintainers-guide">Maintainers</a> are responsible for oversight of this project's community development activities, including evaluation of GitHub <a href="https://github.com/oasis-open/openc2-lycan-python/blob/master/CONTRIBUTING.md#fork-and-pull-collaboration-model">pull requests</a> and <a href="https://www.oasis-open.org/policies-guidelines/open-repositories#repositoryManagement">preserving</a> open source principles of openness and fairness. Maintainers are recognized and trusted experts who serve to implement community goals and consensus design preferences.</p>

<p>Initially, the associated TC members have designated one or more persons to serve as Maintainer(s); subsequently, participating community members may select additional or substitute Maintainers, per <a href="https://www.oasis-open.org/resources/open-repositories/maintainers-guide#additionalMaintainers">consensus agreements</a>.</p>

<p><b><a id="currentMaintainers">Current Maintainers of this TC Open Repository</a></b></p>

<ul>
<li><a href="mailto:mstair@att.com">Michael Stair</a>; GitHub ID: <a href="https://github.com/mstair/">https://github.com/mstair/</a>; WWW: <a href="https://www.att.com/">AT&amp;T</a></li>
</ul>

</div>

<div><h2><a id="aboutOpenRepos">About OASIS TC Open Repositories</a></h2>

<p><ul>
<li><a href="https://www.oasis-open.org/resources/open-repositories/">TC Open Repositories: Overview and Resources</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/faq">Frequently Asked Questions</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/licenses">Open Source Licenses</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/cla">Contributor License Agreements (CLAs)</a></li>
<li><a href="https://www.oasis-open.org/resources/open-repositories/maintainers-guide">Maintainers' Guidelines and Agreement</a></li>
</ul></p>

</div>

<div><h2><a id="feedback">Feedback</a></h2>

<p>Questions or comments about this TC Open Repository's activities should be composed as GitHub issues or comments. If use of an issue/comment is not possible or appropriate, questions may be directed by email to the Maintainer(s) <a href="#currentMaintainers">listed above</a>.  Please send general questions about TC Open Repository participation to OASIS Staff at <a href="mailto:repository-admin@oasis-open.org">repository-admin@oasis-open.org</a> and any specific CLA-related questions to <a href="mailto:repository-cla@oasis-open.org">repository-cla@oasis-open.org</a>.</p>

</div>
