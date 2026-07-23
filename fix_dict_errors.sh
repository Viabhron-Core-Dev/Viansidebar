sed -i 's/androidx.lifecycle.lifecycleScope/lifecycleScope/g' app/src/main/java/com/example/DictionaryImportActivity.kt
sed -i '/import androidx.activity.ComponentActivity/a import androidx.lifecycle.lifecycleScope' app/src/main/java/com/example/DictionaryImportActivity.kt

sed -i 's/androidx.compose.foundation.rememberScrollState()/rememberScrollState()/g' app/src/main/java/com/example/service/DictionaryPageView.kt
sed -i 's/androidx.compose.foundation.verticalScroll/verticalScroll/g' app/src/main/java/com/example/service/DictionaryPageView.kt
sed -i '/import androidx.compose.foundation.lazy.items/a import androidx.compose.foundation.rememberScrollState\nimport androidx.compose.foundation.verticalScroll' app/src/main/java/com/example/service/DictionaryPageView.kt

sed -i 's/androidx.compose.foundation.rememberScrollState()/rememberScrollState()/g' app/src/main/java/com/example/service/DictionaryPopupActivity.kt
sed -i 's/androidx.compose.foundation.verticalScroll/verticalScroll/g' app/src/main/java/com/example/service/DictionaryPopupActivity.kt
sed -i '/import androidx.compose.foundation.layout.*/a import androidx.compose.foundation.rememberScrollState\nimport androidx.compose.foundation.verticalScroll' app/src/main/java/com/example/service/DictionaryPopupActivity.kt

sed -i 's/androidx.compose.foundation.rememberScrollState()/rememberScrollState()/g' app/src/main/java/com/example/service/DictionaryWindowManager.kt
sed -i 's/androidx.compose.foundation.verticalScroll/verticalScroll/g' app/src/main/java/com/example/service/DictionaryWindowManager.kt
sed -i '/import androidx.compose.foundation.lazy.items/a import androidx.compose.foundation.rememberScrollState\nimport androidx.compose.foundation.verticalScroll' app/src/main/java/com/example/service/DictionaryWindowManager.kt
