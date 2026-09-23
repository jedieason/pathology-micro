package com.jedieason.pathologymicro

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.jedieason.pathologymicro.data.repository.CaseRepository
import com.jedieason.pathologymicro.ui.MicroScreen
import com.jedieason.pathologymicro.ui.theme.MicroTheme

class MainActivity : ComponentActivity() {

    private lateinit var repository: CaseRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        repository = CaseRepository(this)

        setContent {
            MicroTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    MicroScreen(repository = repository)
                }
            }
        }
    }
}
