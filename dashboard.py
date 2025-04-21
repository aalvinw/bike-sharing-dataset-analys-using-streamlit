import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/aalvinw/bike-sharing-dataset-analys-using-streamlit/refs/heads/main/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/aalvinw/bike-sharing-dataset-analys-using-streamlit/refs/heads/main/hour.csv")

# Rename kolom
day_df.rename(columns={"cnt": "count_rent"}, inplace=True)
hour_df.rename(columns={"cnt": "count_rent"}, inplace=True)

# Konversi dteday jadi datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Sidebar untuk rentang tanggal
st.sidebar.title("Pilih Rentang Tanggal")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

start_date = st.sidebar.date_input("Tanggal Awal", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input("Tanggal Akhir", min_value=min_date, max_value=max_date, value=max_date)

# Filter berdasarkan tanggal
filtered_day_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & (day_df["dteday"] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & (hour_df["dteday"] <= pd.to_datetime(end_date))]

# Judul dashboard
st.title("Dashboard Penyewaan Sepeda")

# Visualisasi 1: Cuaca vs Penyewaan
st.subheader("Jumlah Penyewaan Berdasarkan Cuaca")
sum_weather_df = filtered_day_df.groupby("weathersit").agg({"count_rent": "sum"}).reset_index()
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Sort descending
df_sorted1 = sum_weather_df.sort_values(by="count_rent", ascending=False)

sns.barplot(
    x="weathersit",
    y="count_rent",
    data=df_sorted1,
    order=df_sorted1["weathersit"],
    palette=sns.color_palette("Blues_r", len(df_sorted1)),
    ax=ax[0]
)

ax[0].set_ylabel(None)
ax[0].set_xlabel("Weathersit", fontsize=30)
ax[0].set_title("Cuaca dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
ax[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Sort ascending
df_sorted2 = sum_weather_df.sort_values(by="count_rent", ascending=True).iloc[::-1]

sns.barplot(
    x="weathersit",
    y="count_rent",
    data=df_sorted2,
    order=df_sorted2["weathersit"],
    palette=sns.color_palette("Blues", len(df_sorted2)),
    ax=ax[1]
)

ax[1].set_ylabel(None)
ax[1].set_xlabel("Weathersit", fontsize=30)
ax[1].set_title("Cuaca dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
ax[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

st.pyplot(fig)
# Visualisasi 2: Musim vs Penyewaan
st.subheader("Jumlah Penyewaan Berdasarkan Musim")
sum_season_df = filtered_day_df.groupby("season").agg({"count_rent": "sum"}).reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(data=sum_season_df, x="season", y="count_rent", palette="coolwarm", ax=ax2)
ax2.set_ylabel("Jumlah Penyewa")
ax2.set_xlabel("Musim")
ax2.set_xticklabels(["Semi", "Panas", "Gugur", "Dingin"])
st.pyplot(fig2)

# Visualisasi 3: Line Chart per Tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

weather_labels = {1: "Clear", 2: "Misty", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_colors = {1: "#FF9999", 2: "#90CAF9", 3: "#FFD700", 4: "#A0A0A0"}

day_df['weather_label'] = day_df['weathersit'].map(weather_labels)
day_df['season_label'] = day_df['season'].map(season_labels)

# Grup data
weather_season_counts = day_df.groupby(["dteday", "weathersit", "season"])["count_rent"].sum().reset_index()

# Streamlit Title
st.title("Jumlah Penyewa Sepeda Berdasarkan Cuaca dan Musim")

# Plot
fig, ax = plt.subplots(figsize=(24, 5))

for weather_type, weather_label in weather_labels.items():
    for season_type, season_label in season_labels.items():
        subset = weather_season_counts[
            (weather_season_counts["weathersit"] == weather_type) &
            (weather_season_counts["season"] == season_type)
        ]
        ax.scatter(
            subset["dteday"],
            subset["count_rent"],
            s=10,
            label=f"{weather_label} - {season_label}",
            color=season_colors[season_type]
        )

sns.lineplot(x="dteday", y="count_rent", hue="weathersit", data=weather_season_counts, linewidth=1.5, ax=ax)

ax.set_xlabel('Tahun (2012)')
ax.set_ylabel('Jumlah Penyewa')
ax.set_title('Grafik Jumlah Penyewa Sepeda Berdasarkan Cuaca dan Musim')
ax.legend(title="Cuaca - Musim", loc="upper left", bbox_to_anchor=(1, 1))

# Tampilkan di Streamlit
st.pyplot(fig)

# Visualisasi 4: Rata-rata Penyewaan per Jam
# Misalnya ubah nama kolom kalau belum sesuai
hour_df.rename(columns={"hr": "hour", "cnt": "count_rent"}, inplace=True)

# Judul Halaman Streamlit
st.title("Rata-rata Penyewaan Sepeda per Jam dalam Sehari")

# Buat plot
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hour_df["hour"], y=hour_df["count_rent"], ci=None, marker="o", color="blue", ax=ax)

ax.set_title("Rata-rata Penyewaan Sepeda per Jam dalam Sehari")
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_xticks(range(0, 24))

# Tampilkan plot di Streamlit
st.pyplot(fig)


# Visualisasi 5: Pie chart Casual vs Registered
st.subheader("Proporsi Casual vs Registered")
casual = filtered_day_df["casual"].sum()
registered = filtered_day_df["registered"].sum()
fig5, ax5 = plt.subplots()
ax5.pie([casual, registered], labels=["Casual", "Registered"], autopct="%1.1f%%", colors=["#FFD700", "#00BFFF"])
st.pyplot(fig5)
