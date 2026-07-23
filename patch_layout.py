with open("app/src/main/res/layout/layout_floating_reader.xml", "r") as f:
    content = f.read()

old_bubble = """    <!-- FOLDED STATE (BUBBLE) -->
    <TextView
        android:id="@+id/bubble_icon"
        android:layout_width="36dp"
        android:layout_height="36dp"
        android:background="@drawable/ic_bubble_round"
        android:text="v"
        android:textSize="20sp"
        android:textColor="#9C27B0"
        android:alpha="0.3"
        android:gravity="center"
        android:elevation="8dp"
        android:includeFontPadding="false"
        android:paddingBottom="2dp"
        android:visibility="gone" />"""
new_bubble = """    <!-- FOLDED STATE (BUBBLE) -->
    <TextView
        android:id="@+id/bubble_icon"
        android:layout_width="48dp"
        android:layout_height="48dp"
        android:background="@drawable/bg_circle_reader"
        android:text="E"
        android:textSize="20sp"
        android:textColor="#FFFFFF"
        android:textStyle="bold"
        android:gravity="center"
        android:elevation="8dp"
        android:visibility="gone" />"""
content = content.replace(old_bubble, new_bubble)

with open("app/src/main/res/layout/layout_floating_reader.xml", "w") as f:
    f.write(content)
