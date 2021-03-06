# Tests and feedbacks

## Version 0.2

*Approach*: aiming touch position to target position (pos += (target - pos) / 4.)

- Lucie (Galaxy S5): interaction are broken, like she have water on the screen
- Kovak (LG 4G): Scrolling appears smoother but interaction are actually harder or just not triggered
- Mathieu (One Plus 3t): Smooth scrolling but velocity is broken = interaction broken
- Arnaud (Nexus 5): It is harder to get fast on the list

**Conclusion**: the velocity lost break all the basic interaction, and scrolling
to the list require more swipes.

## Version 0.3

*Approach*: Use KinectEffect to compute velocity each time an input is received.
When no input are available on a frame, use the velocity to predict where the cursor may be in the current frame.
When no input are received in 0.1ms, decrease the velocity by half every frame.

- Lucie (Galaxy S5): Better, can see the difference, but there are mistake on the carousel.
- Arnaud (Nexus 5): Doesn't see the difference between raw and smooth, as the raw version works very well
- Mathieu (One Plus 3t): Smooth scrolling, velocity seems preserved (i can go to the same element on raw or smooth if i drag at the same speed). Low movement seems erratic
- Gabriel (xiaomi redmi 3 pro): Not sure which is better; when swiping, both seems smooth; when shaking (l/r or t/u) it feels more erratic, the delay is more noticable.

**Conclusion**: velocity seems ok now, on good device, there is no difference between
raw, and the issues became more about the behavior of the widget itself (like the carousel
should use the velocity instead of doing static animation to the next or previous).
And the recycleview should have a better maximum velocity or less friction i guess.

## Version 0.4

*Approach*: Nothing changed in the core of the SmoothTouch. The smooth touch carousel version is rebuild in top of
touch velocity instead of a pre-defined animation. The RecycleView have friction reduced from 0.05 to 0.015.
Mapview works now (was missing INTERNET permission before).

- Mathieu (One Plus 3t): Carousel is fantastic and fast. RecycleView movement doesn't have the "right" velocity when
i do fast movement, but unsure if it's related to us or the system. If i do a long movement, it look like it works
well.
- Gabriel (xiaomi redmi 3 pro): Like the carousel, no difference on Mapview. Hard to get speed on recycleview.
- Kived (?): Carousel should go to the nearest slide; no difference on mapview, harder to get inertia on the list, and both need greater damping for low value
- Arnaud (Nexus 5): Carousel and recycleview are more reactive
- Lucie (Galaxy S5): The carousel don't have "smooth" as the first one, it is more fast and stop without slowing down. Don't see any difference in the RecycleView.

**Conclusion**: The new carousel is definitively the way to go. It seems that the whole things is unecessary on some phones: i can clearly see the drag difference between the Galaxy S5 and One Plus 3t: the One Plus shutter much more than the Galaxy S5 on the raw touches. But only in "Kivy" app, nothing can be seen in native lists: which mean somehow they implement a similar algorithm (guessing, not verified).
