# Minutes Crawler

Currently, I am the Recording Secretary for my fraternity, so I decided to write a script to look through the minutes I've been writing and find some trends. This script determines how many times someone speaks and makes a motion during a meeting, as well as the lengths of various sections within the meeting and the meeting overall.

<b>For the crawler to work, it acts under the following assumptions:</b>
<ul>
  <li>There is a well-defined roster of all members in a file called <b>roster.txt</b>.</li>
  <li>The minutes files to inspect are in a directory called <b>minutes</b>.</li>
  <li>When someone speaks, it is recorded in the format "NAME:".</li>
  <li>When someone makes a motion, it is recorded in the format "<i>NAME</i>: <i>MOTION</i> (seconded and passed)".</li>
  <li>The meeting contains the sections <i>Committee Business, Unfinished Business, New Business, Special Orders,</i> and <i>Announcements.</i></li>
  <li>The start time of the meeting is declared as "Called to order at <i>TIME</i>".</li>
  <li>The end of the meeting is declared as "Adjournment (<i>TIME</i>)".</li>
</ul>

These are a lot of formatting specifics, but when the file is in the correct format, you will get interesting statistics from a meeting!
