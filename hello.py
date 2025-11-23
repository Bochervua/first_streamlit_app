import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Настройка страницы
st.set_page_config(
    page_title="College Marks Analyzer",
    page_icon="🎓",
    layout="wide"
)

# Заголовок
st.title("🎓 College Marks Dataset Analyzer")
st.markdown("---")


# Загрузка данных
@st.cache_data
def load_data():
    return pd.read_csv('College_Marks_Dataset.csv')


try:
    data = load_data()
    st.success("✅ Данные успешно загружены!")
except:
    st.error("❌ Ошибка загрузки данных. Убедитесь, что файл существует.")
    st.stop()

# 📊 КОНТРОЛ 1: Боковая панель с фильтрами
st.sidebar.header("🔧 Фильтры и настройки")

# Фильтр по колонкам
selected_columns = st.sidebar.multiselect(
    "Выберите колонки для отображения:",
    options=data.columns.tolist(),
    default=data.columns.tolist()[:5]
)

# 📊 КОНТРОЛ 2: Слайдер для выборки данных
sample_size = st.sidebar.slider(
    "Размер выборки:",
    min_value=10,
    max_value=len(data),
    value=min(100, len(data)),
    step=10
)

# 📊 КОНТРОЛ 3: Радиокнопки для типа отображения
view_mode = st.sidebar.radio(
    "Режим отображения:",
    ["📋 Таблица", "📊 Статистика", "📈 Визуализация"]
)

# Основная область контента
if view_mode == "📋 Таблица":
    st.header("📋 Исходные данные")

    # 📊 КОНТРОЛ 4: Поиск по данным
    search_term = st.text_input("🔍 Поиск по данным:", "")

    display_data = data[selected_columns].head(sample_size)

    if search_term:
        mask = display_data.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_data = display_data[mask]

    st.dataframe(display_data, use_container_width=True)

    # Информация о данных
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Всего записей", len(data))
    with col2:
        st.metric("Колонок", data.shape[1])
    with col3:
        st.metric("Пропущенных значений", data.isnull().sum().sum())

elif view_mode == "📊 Статистика":
    st.header("📊 Статистический анализ")

    # Выбор колонки для анализа
    numeric_cols = data.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        selected_stat_col = st.selectbox("Выберите колонку для анализа:", numeric_cols)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Базовая статистика")
            st.write(data[selected_stat_col].describe())

        with col2:
            st.subheader("Распределение")
            fig = px.histogram(data, x=selected_stat_col, title=f"Распределение {selected_stat_col}")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("В данных нет числовых колонок для анализа")

else:  # Визуализация
    st.header("📈 Визуализация данных")

    # 📊 КОНТРОЛ 5: Выбор типа графика
    chart_type = st.selectbox(
        "Тип графика:",
        ["Гистограмма", "Box Plot", "Scatter Plot", "Line Chart"]
    )

    numeric_cols = data.select_dtypes(include=['number']).columns

    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            x_axis = st.selectbox("Ось X:", numeric_cols)
        with col2:
            y_axis = st.selectbox("Ось Y:", numeric_cols)

        if chart_type == "Гистограмма" and x_axis:
            fig = px.histogram(data, x=x_axis, title=f"Гистограмма {x_axis}")
        elif chart_type == "Box Plot" and x_axis:
            fig = px.box(data, y=x_axis, title=f"Box Plot {x_axis}")
        elif chart_type == "Scatter Plot" and x_axis and y_axis:
            fig = px.scatter(data, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
        elif chart_type == "Line Chart" and x_axis and y_axis:
            fig = px.line(data.head(50), x=x_axis, y=y_axis, title=f"Line Chart: {x_axis} vs {y_axis}")
        else:
            fig = go.Figure()
            fig.update_layout(title="Выберите параметры для графика")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Недостаточно числовых колонок для визуализации")

# Футер
st.markdown("---")
st.markdown("### 📊 College Marks Dataset Analyzer")
st.markdown("Created with ❤️ using Streamlit")