import os

with open("app/src/main/java/com/example/service/ScreenRecordService.kt", "r") as f:
    content = f.read()

old_res = """            if (quality == 720) {
                screenWidth = (screenWidth * (720f / screenHeight)).toInt()
                screenHeight = 720
            } else if (quality == 1080) {
                screenWidth = (screenWidth * (1080f / screenHeight)).toInt()
                screenHeight = 1080
            }
            
            // Ensure even numbers
            screenWidth = if (screenWidth % 2 != 0) screenWidth - 1 else screenWidth
            screenHeight = if (screenHeight % 2 != 0) screenHeight - 1 else screenHeight"""

new_res = """            val isPortrait = screenHeight > screenWidth
            val smallerDim = if (isPortrait) screenWidth else screenHeight
            val largerDim = if (isPortrait) screenHeight else screenWidth
            
            var targetSmaller = smallerDim
            if (quality == 720 && smallerDim > 720) {
                targetSmaller = 720
            } else if (quality == 1080 && smallerDim > 1080) {
                targetSmaller = 1080
            }
            
            val scale = targetSmaller.toFloat() / smallerDim.toFloat()
            var targetLarger = (largerDim * scale).toInt()
            
            // Make them multiples of 16 for better encoder compatibility
            targetSmaller = (targetSmaller / 16) * 16
            targetLarger = (targetLarger / 16) * 16
            
            if (isPortrait) {
                screenWidth = targetSmaller
                screenHeight = targetLarger
            } else {
                screenWidth = targetLarger
                screenHeight = targetSmaller
            }"""

content = content.replace(old_res, new_res)

with open("app/src/main/java/com/example/service/ScreenRecordService.kt", "w") as f:
    f.write(content)
