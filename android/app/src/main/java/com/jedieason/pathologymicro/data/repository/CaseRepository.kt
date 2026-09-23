package com.jedieason.pathologymicro.data.repository

import android.content.Context
import android.content.SharedPreferences
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.jedieason.pathologymicro.data.model.CaseData
import com.jedieason.pathologymicro.data.model.UserRecord
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL

class CaseRepository(private val context: Context) {

    private val gson = Gson()
    private val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    private val cacheFile = File(context.filesDir, CACHE_FILE_NAME)

    companion object {
        private const val PREFS_NAME = "micro_practice_prefs"
        private const val STORAGE_KEY = "micro-practice-v1"
        private const val CACHE_FILE_NAME = "cases_cache.json"

        const val GITHUB_PAGES_CASES_URL = "https://jedieason.github.io/pathology-micro/data/cases.json"
        const val GITHUB_RAW_CASES_URL = "https://raw.githubusercontent.com/jedieason/pathology-micro/main/data/cases.json"
        const val BASE_IMAGE_URL = "https://jedieason.github.io/pathology-micro/"
    }

    fun resolveImageUrl(relativeOrAbsoluteSrc: String): String {
        return if (relativeOrAbsoluteSrc.startsWith("http://") || relativeOrAbsoluteSrc.startsWith("https://")) {
            relativeOrAbsoluteSrc
        } else {
            val cleanPath = relativeOrAbsoluteSrc.removePrefix("/")
            "$BASE_IMAGE_URL$cleanPath"
        }
    }

    suspend fun loadInitialCases(): CaseData = withContext(Dispatchers.IO) {
        if (cacheFile.exists() && cacheFile.length() > 0) {
            try {
                cacheFile.reader().use { reader ->
                    val data = gson.fromJson(reader, CaseData::class.java)
                    if (data != null && data.cases.isNotEmpty()) {
                        return@withContext data
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }

        // Fallback to bundled asset
        context.assets.open("data/cases.json").use { stream ->
            InputStreamReader(stream).use { reader ->
                gson.fromJson(reader, CaseData::class.java)
            }
        }
    }

    suspend fun syncCasesFromRemote(): Result<CaseData> = withContext(Dispatchers.IO) {
        val urlsToTry = listOf(GITHUB_PAGES_CASES_URL, GITHUB_RAW_CASES_URL)
        var lastException: Exception? = null

        for (urlString in urlsToTry) {
            try {
                val url = URL(urlString)
                val conn = (url.openConnection() as HttpURLConnection).apply {
                    connectTimeout = 8000
                    readTimeout = 8000
                    requestMethod = "GET"
                    setRequestProperty("Accept", "application/json")
                }
                if (conn.responseCode in 200..299) {
                    val jsonText = conn.inputStream.bufferedReader().use { it.readText() }
                    val data = gson.fromJson(jsonText, CaseData::class.java)
                    if (data != null && data.cases.isNotEmpty()) {
                        // Update local cache
                        cacheFile.writeText(jsonText)
                        return@withContext Result.success(data)
                    }
                }
            } catch (e: Exception) {
                lastException = e
            }
        }

        Result.failure(lastException ?: Exception("Failed to fetch cases from remote"))
    }

    fun loadRecords(): MutableMap<String, UserRecord> {
        val json = prefs.getString(STORAGE_KEY, null) ?: return mutableMapOf()
        return try {
            val type = object : TypeToken<Map<String, UserRecord>>() {}.type
            val map: Map<String, UserRecord>? = gson.fromJson(json, type)
            map?.toMutableMap() ?: mutableMapOf()
        } catch (e: Exception) {
            mutableMapOf()
        }
    }

    fun saveRecords(records: Map<String, UserRecord>) {
        val json = gson.toJson(records)
        prefs.edit().putString(STORAGE_KEY, json).apply()
    }

    fun clearRecords() {
        prefs.edit().remove(STORAGE_KEY).apply()
    }
}
