cat << 'INNER_EOF' > script.awk
/fun showSidebarEditOverlay\(\)/ {
    inSidebar = 1
    print
    next
}
inSidebar && /onAddClicked = \{/ {
    print "            onAddClicked = { "
    print "                showAddElementOverlayForSelection { id ->"
    print "                    com.example.LogKeeper.writeLog(\"SidebarEdit\", \"Added new element: $id\")"
    print "                    sidebarEditOverlayView?.localIds?.add(id)"
    print "                    sidebarEditOverlayView?.refresh()"
    print "                }"
    print "            },"
    skip = 1
    next
}
inSidebar && skip && /},/ {
    skip = 0
    next
}
skip { next }
{ print }
INNER_EOF
awk -f script.awk app/src/main/java/com/example/service/FloatingReaderService.kt > tmp.kt
mv tmp.kt app/src/main/java/com/example/service/FloatingReaderService.kt
