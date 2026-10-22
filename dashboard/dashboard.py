"""
Bike Sharing Analytics Dashboard
================================
Interactive Streamlit dashboard for analyzing historical bike sharing data (2011-2012).
Developed according to Python and Streamlit best practices.
"""

from pathlib import Path
from typing import Tuple
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
REMOTE_DATA_URL = (
    "https://raw.githubusercontent.com/MHendriF/bike-sharing-analysis/main/dashboard/main_data.csv"
)
REMOTE_LOGO_URL = (
    "https://raw.githubusercontent.com/MHendriF/bike-sharing-analysis/main/assets/bycicle.png"
)

LOCAL_DATA_PATH = Path(__file__).resolve().parent / "main_data.csv"
LOCAL_LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "bycicle.png"

SEASON_CATEGORIES = ["Spring", "Summer", "Fall", "Winter"]
WEATHER_CATEGORIES = ["good", "moderate", "bad", "worse"]
MONTH_CATEGORIES = [
    "Jan", "Feb", "Mar", "Apr", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec"
]
HOURLY_CATEGORIES = [
    "12 am", "01 am", "02 am", "03 am", "04 am", "05 am",
    "06 am", "07 am", "08 am", "09 am", "10 am", "11 am",
    "12 pm", "01 pm", "02 pm", "03 pm", "04 pm", "05 pm",
    "06 pm", "07 pm", "08 pm", "09 pm", "10 pm", "11 pm"
]

sns.set_theme(style="whitegrid")


# ==============================================================================
# DATA LOADING & CACHING
# ==============================================================================
@st.cache_data(show_spinner=True)
def load_data() -> pd.DataFrame:
    """Load and preprocess the bike sharing dataset.

    Attempts to load from the local filesystem first. If the file is not found,
    falls back to the GitHub raw data URL.

    Returns:
        pd.DataFrame: Preprocessed DataFrame with parsed dates.
    """
    if LOCAL_DATA_PATH.exists():
        df = pd.read_csv(LOCAL_DATA_PATH)
    else:
        df = pd.read_csv(REMOTE_DATA_URL)

    df["date"] = pd.to_datetime(df["date"])
    df.sort_values(by="date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# ==============================================================================
# DATA AGGREGATION HELPERS
# ==============================================================================
def create_seasonly_users_df(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total bike users grouped by season and year.

    Args:
        df: Filtered bike sharing DataFrame.

    Returns:
        pd.DataFrame: Seasonally aggregated DataFrame ordered by season.
    """
    aggregated = df.groupby(["season", "year"], observed=False).agg(
        total_users=("total_users", "sum")
    ).reset_index()
    aggregated["season"] = pd.Categorical(
        aggregated["season"], categories=SEASON_CATEGORIES, ordered=True
    )
    return aggregated.sort_values("season")


def create_weather_cond_users_df(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total bike users grouped by weather situation and year.

    Args:
        df: Filtered bike sharing DataFrame.

    Returns:
        pd.DataFrame: Weather-aggregated DataFrame ordered by severity.
    """
    aggregated = df.groupby(["weather_situation", "year"], observed=False).agg(
        total_users=("total_users", "sum")
    ).reset_index()
    aggregated["weather_situation"] = pd.Categorical(
        aggregated["weather_situation"], categories=WEATHER_CATEGORIES, ordered=True
    )
    return aggregated.sort_values("weather_situation")


def create_monthly_users_df(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total bike users grouped by month and year.

    Args:
        df: Filtered bike sharing DataFrame.

    Returns:
        pd.DataFrame: Monthly aggregated DataFrame ordered chronologically.
    """
    aggregated = df.groupby(["month", "year"], observed=False).agg(
        total_users=("total_users", "sum")
    ).reset_index()
    aggregated["month"] = pd.Categorical(
        aggregated["month"], categories=MONTH_CATEGORIES, ordered=True
    )
    return aggregated.sort_values("month")


def create_hourly_users_df(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total bike users grouped by hour of the day.

    Args:
        df: Filtered bike sharing DataFrame.

    Returns:
        pd.DataFrame: Hourly aggregated DataFrame ordered chronologically.
    """
    aggregated = df.groupby(["hour"], observed=False).agg(
        total_users=("total_users", "sum")
    ).reset_index()
    aggregated["hour"] = pd.Categorical(
        aggregated["hour"], categories=HOURLY_CATEGORIES, ordered=True
    )
    return aggregated.sort_values("hour")


def create_composition_users_df(df: pd.DataFrame) -> pd.Series:
    """Calculate the total composition of casual vs registered users.

    Args:
        df: Filtered bike sharing DataFrame.

    Returns:
        pd.Series: Aggregated counts of casual and registered users.
    """
    return df[["casual_users", "registered_users"]].sum()


# ==============================================================================
# UI COMPONENTS & PLOTTING HELPERS
# ==============================================================================
def render_metrics(filtered_df: pd.DataFrame) -> None:
    """Display high-level KPI cards for rentals."""
    total_casual = filtered_df["casual_users"].sum()
    total_registered = filtered_df["registered_users"].sum()
    total_rides = filtered_df["total_users"].sum()
    avg_daily_rides = int(filtered_df.groupby("date")["total_users"].sum().mean()) if not filtered_df.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Semua Penyewaan",
            value=f"{total_rides:,}",
            help="Total penyewaan sepeda (kasual + terdaftar) pada rentang data terpilih."
        )
    with col2:
        reg_pct = (total_registered / total_rides * 100) if total_rides > 0 else 0
        st.metric(
            label="Pengguna Terdaftar (Registered)",
            value=f"{total_registered:,}",
            delta=f"{reg_pct:.1f}% dari total"
        )
    with col3:
        cas_pct = (total_casual / total_rides * 100) if total_rides > 0 else 0
        st.metric(
            label="Pengguna Kasual (Casual)",
            value=f"{total_casual:,}",
            delta=f"{cas_pct:.1f}% dari total"
        )
    with col4:
        st.metric(
            label="Rata-rata Penyewaan / Hari",
            value=f"{avg_daily_rides:,}",
            help="Rata-rata total sepeda yang disewa per hari dalam periode terpilih."
        )


def plot_seasonal_trends(seasonly_df: pd.DataFrame) -> None:
    """Render seasonal rental comparison bar plot."""
    st.subheader("Tren Penyewaan Berdasarkan Musim (2011 vs 2012)")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(
        data=seasonly_df,
        x="season",
        y="total_users",
        hue="year",
        palette="viridis",
        errorbar=None,
        ax=ax,
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", fontsize=10, padding=3)

    ax.set_title("Total Pengguna Sepeda di Setiap Musim", fontsize=14, pad=12)
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Total Pengguna (Rides)", fontsize=12)
    ax.tick_params(axis="both", labelsize=11)
    ax.yaxis.set_major_formatter("{x:,.0f}")
    ax.legend(title="Tahun", loc="upper left")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "💡 **Insight Bisnis:** Musim Gugur (**Fall**) merupakan musim dengan penyewaan tertinggi baik pada 2011 "
        "maupun 2012 (mencapai 641,479 penyewaan pada 2012). Sebaliknya, musim semi (**Spring**) memiliki volume "
        "terendah. Terdapat pertumbuhan konsisten di semua musim dari 2011 ke 2012."
    )


def plot_weather_trends(weather_df: pd.DataFrame) -> None:
    """Render weather condition comparison bar plot."""
    st.subheader("Pengaruh Kondisi Cuaca Terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(
        data=weather_df,
        x="weather_situation",
        y="total_users",
        hue="year",
        palette="crest",
        errorbar=None,
        ax=ax,
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", fontsize=10, padding=3)

    ax.set_title("Total Pengguna Berdasarkan Situasi Cuaca", fontsize=14, pad=12)
    ax.set_xlabel("Kondisi Cuaca (Good / Moderate / Bad / Worse)", fontsize=12)
    ax.set_ylabel("Total Pengguna (Rides)", fontsize=12)
    ax.tick_params(axis="both", labelsize=11)
    ax.yaxis.set_major_formatter("{x:,.0f}")
    ax.legend(title="Tahun", loc="upper right")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "💡 **Insight Bisnis:** Cuaca cerah/sebagian berawan (**good**) mendominasi secara absolut dengan lebih dari "
        "1.46 juta penyewaan di 2012. Saat cuaca ekstrem/buruk (**worse**), penyewaan anjlok drastis ke angka di bawah 200, "
        "menandakan operasi sangat sensitif terhadap prakiraan cuaca."
    )


def plot_monthly_trends(monthly_df: pd.DataFrame) -> None:
    """Render monthly trend line plot."""
    st.subheader("Tren Perkembangan Pengguna Sepeda Setiap Bulan (2011 vs 2012)")
    fig, ax = plt.subplots(figsize=(14, 5.5))

    sns.lineplot(
        x="month",
        y="total_users",
        hue="year",
        data=monthly_df,
        marker="o",
        palette="magma",
        markersize=8,
        linewidth=2.5,
        ax=ax,
    )

    ax.set_title("Fluktuasi Bulanan Penyewaan Sepeda", fontsize=14, pad=12)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Total Pengguna (Rides)", fontsize=12)
    ax.tick_params(axis="both", labelsize=11)
    ax.yaxis.set_major_formatter("{x:,.0f}")
    ax.legend(title="Tahun", loc="upper left")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "💡 **Insight Bisnis:** Pada 2011, puncak terjadi di bulan **Juni** (143,512). Sementara pada 2012, tren naik "
        "bertahan lebih lama hingga mencapai puncaknya di bulan **September** (218,573). Tren selalu menurun di kuartal akhir "
        "(November-Desember) akibat perubahan temperatur menuju musim dingin."
    )


def plot_hourly_traffic(hourly_df: pd.DataFrame) -> None:
    """Render horizontal bar plot of hourly traffic patterns."""
    st.subheader("Distribusi Traffic Penyewaan Berdasarkan Jam Operasional")
    fig, ax = plt.subplots(figsize=(13, 8))

    # Highlight peak hours with different color intensity
    colors = ["#2b5c8f" if h in ["08 am", "05 pm", "06 pm"] else "#90caf9" for h in hourly_df["hour"]]

    sns.barplot(
        data=hourly_df,
        x="total_users",
        y="hour",
        palette=colors,
        hue="hour",
        legend=False,
        orient="h",
        ax=ax,
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", fontsize=9, padding=4)

    ax.set_title("Pola Jam Sibuk Penyewaan Sepeda (Peak Hours: 08:00 AM & 05:00-06:00 PM)", fontsize=14, pad=12)
    ax.set_xlabel("Total Pengguna (Rides)", fontsize=12)
    ax.set_ylabel("Waktu (Jam)", fontsize=12)
    ax.tick_params(axis="both", labelsize=10)
    ax.xaxis.set_major_formatter("{x:,.0f}")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "💡 **Insight Bisnis:** Terlihat pola komuter (commuter pattern) yang sangat kuat. Puncak penyewaan terjadi pada "
        "jam berangkat kerja (**08:00 AM**) dan jam pulang kerja (**05:00 PM - 06:00 PM** dengan rekor tertinggi 336,860 rides). "
        "Titik terendah berada pada pukul **04:00 AM** (4,428 rides)."
    )


def plot_user_composition(composition_series: pd.Series) -> None:
    """Render donut chart of user composition."""
    st.subheader("Proporsi Pengguna: Casual vs Registered")
    fig, ax = plt.subplots(figsize=(6, 6))

    labels = ["Casual Users", "Registered Users"]
    values = [composition_series.get("casual_users", 0), composition_series.get("registered_users", 0)]
    colors = ["#f39c12", "#27ae60"]

    wedges, texts, autotexts = ax.pie(
        x=values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(12)
        autotext.set_weight("bold")

    ax.set_title("Komposisi Segmen Pelanggan", fontsize=14, pad=12)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "💡 **Insight Bisnis:** Layanan didominasi secara signifikan oleh **pengguna terdaftar (Registered: ~81.2%)**, "
        "sedangkan pengguna kasual menyumbang **~18.8%**. Strategi bisnis yang efektif mencakup konversi pengguna kasual "
        "menjadi member berlangganan melalui program loyalty atau promo hari kerja."
    )


# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title="Bike-Sharing Analytics Dashboard",
        page_icon="🚲",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for polished metric cards and headers
    st.markdown(
        """
        <style>
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #e9ecef;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 15px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    all_df = load_data()

    # --------------------------------------------------------------------------
    # SIDEBAR CONTROLS
    # --------------------------------------------------------------------------
    min_date = all_df["date"].min().date()
    max_date = all_df["date"].max().date()

    with st.sidebar:
        # Render logo (local preferred, remote fallback)
        if LOCAL_LOGO_PATH.exists():
            st.image(str(LOCAL_LOGO_PATH), width=200)
        else:
            st.image(REMOTE_LOGO_URL, width=200)

        st.markdown("### ⚙️ Filter Data")

        # Robust date range input (handles intermediate selection states)
        date_input = st.date_input(
            label="Rentang Tanggal",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            help="Pilih rentang tanggal untuk memfilter seluruh data analitik.",
        )

        if isinstance(date_input, (list, tuple)) and len(date_input) == 2:
            start_date, end_date = date_input
        elif isinstance(date_input, (list, tuple)) and len(date_input) == 1:
            start_date = date_input[0]
            end_date = max_date
        else:
            start_date, end_date = min_date, max_date

        # Additional multi-selection filters
        selected_seasons = st.multiselect(
            "Filter Musim",
            options=SEASON_CATEGORIES,
            default=SEASON_CATEGORIES,
            help="Saring analisis berdasarkan musim tertentu.",
        )

        selected_weather = st.multiselect(
            "Filter Cuaca",
            options=WEATHER_CATEGORIES,
            default=WEATHER_CATEGORIES,
            help="Saring analisis berdasarkan kondisi cuaca.",
        )

        st.markdown("---")
        st.markdown(
            "**Dibuat oleh:**\n"
            "Muhamad Hendri Febriansyah\n\n"
            "[GitHub Repository](https://github.com/MHendriF/bike-sharing-analysis)"
        )

    # --------------------------------------------------------------------------
    # DATA FILTERING
    # --------------------------------------------------------------------------
    filtered_df = all_df[
        (all_df["date"] >= pd.Timestamp(start_date))
        & (all_df["date"] <= pd.Timestamp(end_date))
        & (all_df["season"].isin(selected_seasons))
        & (all_df["weather_situation"].isin(selected_weather))
    ]

    if filtered_df.empty:
        st.warning("⚠️ Tidak ada data yang cocok dengan kriteria filter yang dipilih. Silakan sesuaikan kembali filter.")
        return

    # --------------------------------------------------------------------------
    # HEADER & KPI CARDS
    # --------------------------------------------------------------------------
    st.title("🚲 Bike-Sharing Analytics Dashboard")
    st.caption(
        f"Analisis interaktif penggunaan sepeda sewa dari **{start_date.strftime('%d %b %Y')}** "
        f"hingga **{end_date.strftime('%d %b %Y')}**."
    )

    render_metrics(filtered_df)
    st.markdown("---")

    # --------------------------------------------------------------------------
    # PREPARE AGGREGATED DATA
    # --------------------------------------------------------------------------
    seasonly_users_df = create_seasonly_users_df(filtered_df)
    weather_users_df = create_weather_cond_users_df(filtered_df)
    monthly_users_df = create_monthly_users_df(filtered_df)
    hourly_users_df = create_hourly_users_df(filtered_df)
    composition_users_df = create_composition_users_df(filtered_df)

    # --------------------------------------------------------------------------
    # STRUCTURED TAB NAVIGATION
    # --------------------------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Tren Musiman & Bulanan",
        "⛅ Kondisi Cuaca",
        "⏰ Jam Sibuk (Hourly)",
        "👥 Komposisi Pengguna",
        "📑 Data Mentah",
    ])

    with tab1:
        plot_seasonal_trends(seasonly_users_df)
        st.markdown("---")
        plot_monthly_trends(monthly_users_df)

    with tab2:
        plot_weather_trends(weather_users_df)

    with tab3:
        plot_hourly_traffic(hourly_users_df)

    with tab4:
        col_chart, col_desc = st.columns([1, 1])
        with col_chart:
            plot_user_composition(composition_users_df)
        with col_desc:
            st.markdown("### Ringkasan Segmentasi Pengguna")
            st.write(
                "Pengguna bike sharing terbagi menjadi dua kelompok utama:\n"
                "- **Registered Users (Pelanggan Terdaftar):** Pengguna harian yang memanfaatkan sepeda untuk mobilitas rutin (komuter kerja / sekolah).\n"
                "- **Casual Users (Pengguna Kasual):** Pelancong, turis, atau pengguna akhir pekan yang menyewa secara spontan."
            )
            st.markdown("#### Rekomendasi Bisnis:")
            st.write(
                "1. **Program Konversi Member:** Tawarkan potongan harga langganan bulanan kepada pengguna kasual setelah perjalanan ke-3 mereka.\n"
                "2. **Paket Akhir Pekan:** Rancang paket 'Weekend Explorer' khusus pengguna kasual untuk mendongkrak utilitas armada di luar jam komuter."
            )

    with tab5:
        st.subheader("Eksplorasi Data Terfilter")
        st.dataframe(filtered_df, use_container_width=True)
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Unduh Data Terfilter (CSV)",
            data=csv_data,
            file_name=f"bike_sharing_filtered_{start_date}_{end_date}.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()