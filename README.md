# Tests and feedbacks

## Version 0.2

Algorithm: aiming target position per quarter (pos += (target - pos) / 4.)

- Lucie (Galaxy S5): interaction are broken, like she have water on the screen
- Kovak (?): Scrolling appears smoother but interaction are actually harder or just not triggered
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
