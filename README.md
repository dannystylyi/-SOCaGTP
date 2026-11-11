# README (English)

# Lab: Satellite Orbit Calculation and Ground Track Plotting

## Overview

This project provides functions for calculating an Earth satellite orbit from its initial position and velocity, determining the satellite position and velocity at an arbitrary time, and plotting the satellite ground track on a world map.

The entry point is `labs_solver.py`, which uses the library `orbital_math.py`.

---

## Project Structure

```
.
├── labs_solver.py      # Entry point: orbit element calculation and ground track plotting
└── orbital_math.py     # Orbital mechanics library
```

### Dependencies

- `numpy` — numerical calculations
- `datetime` — date and time handling
- `matplotlib` — plotting
- `cartopy` — map projections and map background

Install:

```bash
pip install numpy matplotlib cartopy
```

---

## Quick Start

```bash
python labs_solver.py
```

Default initial state:
- Position (km): `x = 5700, y = 8500, z = -9000`
- Velocity (km/s): `Vx = -4, Vy = 0, Vz = -3`
- Initial time: `22.08.2025 12:00:00`

---

## Functions in `orbital_math.py`

### Global Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `mu` | `398600` km³/s² | Earth gravitational parameter |
| `omega_earth` | `7.2921159e-5` rad/s | Earth angular velocity |
| `R_earth` | `6371` km | Mean Earth radius |

---

### `orbital_elements(...)`

Calculates orbital elements from initial position and velocity.

**Signature:**

```python
orbital_elements(x=5700, y=8500, z=-9000,
                 Vx=-4, Vy=0, Vz=-3,
                 t0="22.08.2025",
                 printable=False)
```

**Parameters:**
- `x, y, z` — spacecraft center-of-mass coordinates (km);
- `Vx, Vy, Vz` — velocity vector components (km/s);
- `t0` — initial date in `"DD.MM.YYYY"` format (time is set to 12:00:00);
- `printable` — if `True`, prints the results to the console.

**Returns** a dictionary with orbital elements:

| Key | Description |
|-----|-------------|
| `Semi-major axis` | Semi-major axis (km) |
| `Eccentricity` | Eccentricity |
| `Inclination` | Inclination (deg) |
| `Semilatus rectum` | Semi-latus rectum (km) |
| `RAAN` | Right ascension of the ascending node Ω (deg) |
| `Argument of perigee` | Argument of perigee ω (deg) |
| `True anomaly` | True anomaly ν (deg) |
| `Argument of latitude` | Argument of latitude u (deg) |
| `Time since periapsis passage` | Periapsis passage time `t_p` (datetime) |
| `Eccentric anomaly` | Eccentric anomaly E (deg), for elliptical orbits |
| `Hyperbolic anomaly` | Hyperbolic anomaly H (deg), for hyperbolic orbits |
| `Mean anomaly` | Mean anomaly M (deg) |
| `Mean motion` | Mean motion n (rad/s) |
| `Specific orbital energy` | Specific orbital energy h (km²/s²) |
| `Time difference` | Time from periapsis to `t0` (s) |
| `Start time` | Initial time (datetime) |
| `Start position` | Initial radius vector (numpy.array) |

**Orbit type:**
- `h < 0` — elliptical,
- `h == 0` — parabolic,
- `h > 0` — hyperbolic.

---

### `spacecraft_position_velocity(...)`

Calculates spacecraft position and velocity at a given time.

**Signature:**

```python
spacecraft_position_velocity(new_time=5*3600,
                             dict_orbital_elements={},
                             printable=False,
                             main=True)
```

**Parameters:**
- `new_time` — time offset from the initial time in seconds;
- `dict_orbital_elements` — dictionary returned by `orbital_elements()`;
- `printable` — if `True`, prints the results;
- `main` — if `True`, solves Kepler's equation iteratively by fixed-point iteration; otherwise uses the eccentric anomaly from the dictionary.

**Returns:** tuple `(r_vector, V_vector, E_deg)`:
- `r_vector` — radius vector in the geocentric equatorial frame (km);
- `V_vector` — velocity vector (km/s);
- `E_deg` — eccentric anomaly (deg).

**Limitations:**
- Parabolic and hyperbolic orbits are not implemented yet; the function prints a message and returns `None`.

---

### `construct_motion_trajectory(...)`

Plots the satellite ground track and visualizes it on a world map in a cylindrical projection.

**Signature:**

```python
construct_motion_trajectory(orbital_elements={}, k=2, printable=False)
```

**Parameters:**
- `orbital_elements` — dictionary returned by `orbital_elements()`;
- `k` — number of orbital revolutions to display (default `2`);
- `printable` — if `True`, prints ground-track points `[E°, λ°, φ°]` to the console.

**Features:**
- Ground track is calculated with a 1° step in eccentric anomaly;
- Longitude is corrected for Earth rotation using `omega_earth`;
- Track breaks are handled when crossing the ±180° meridian;
- The starting point is marked with a red marker; the start longitude is `l0 = -94.65°`;
- Uses a `cartopy` map background with land, ocean, coastlines, and borders.

---

## Usage Example

```python
import orbital_math as orb

# 1. Calculate orbital elements
elements = orb.orbital_elements(printable=True)

# 2. Position and velocity 5 hours after the start
r, V, E = orb.spacecraft_position_velocity(
    new_time=5*3600,
    dict_orbital_elements=elements,
    printable=True
)

# 3. Plot the ground track for 2 revolutions
orb.construct_motion_trajectory(elements, k=2)
```

---

## Limitations and Notes

- Only elliptical orbits (`e < 1`) are implemented;
- Parabolic and hyperbolic orbits are not supported yet;
- `spacecraft_position_velocity` solves Kepler's equation by fixed-point iteration; convergence is guaranteed for `e < 1`, but the number of iterations may be large when `e` is close to 1;
- Ground-track longitude calculation uses a simplified model: constant Earth angular velocity, without precession or nutation;

---

# README (Русский)

# Лабораторная работа: Расчёт орбиты ИСЗ и построение трассы движения

## Описание

Проект представляет собой набор функций для расчёта орбиты искусственного спутника Земли (ИСЗ) по его начальному положению и скорости, определения положения и скорости КА в произвольный момент времени, а также построения трассы движения на карте мира.

Основной скрипт — `labs_solver.py`, использующий библиотеку `orbital_math.py`.

---

## Структура проекта

```
.
├── labs_solver.py      # Точка входа: расчёт элементов орбиты и построение трассы
└── orbital_math.py     # Библиотека с функциями орбитальной механики
```

### Зависимости

- `numpy` — численные расчёты
- `datetime` — работа с датой и временем
- `matplotlib` — построение графиков
- `cartopy` — картографические проекции и подложка карты

Установка:

```bash
pip install numpy matplotlib cartopy
```

---

## Быстрый старт

```bash
python labs_solver.py
```

По умолчанию используется начальное состояние:
- Положение (км): `x = 5700, y = 8500, z = -9000`
- Скорость (км/с): `Vx = -4, Vy = 0, Vz = -3`
- Начальное время: `22.08.2025 12:00:00`

---

## Функции библиотеки `orbital_math.py`

### Глобальные константы

| Константа | Значение | Описание |
|-----------|----------|----------|
| `mu` | `398600` км³/с² | Гравитационный параметр Земли |
| `omega_earth` | `7.2921159e-5` рад/с | Угловая скорость вращения Земли |
| `R_earth` | `6371` км | Средний радиус Земли |

---

### `orbital_elements(...)`

Вычисляет параметры орбиты по начальным координатам и скорости.

**Сигнатура:**

```python
orbital_elements(x=5700, y=8500, z=-9000,
                 Vx=-4, Vy=0, Vz=-3,
                 t0="22.08.2025",
                 printable=False)
```

**Параметры:**
- `x, y, z` — координаты центра масс КА (км);
- `Vx, Vy, Vz` — компоненты вектора скорости (км/с);
- `t0` — начальная дата в формате `"ДД.ММ.ГГГГ"` (время считается как 12:00:00);
- `printable` — если `True`, выводит результаты в консоль.

**Возвращает** словарь с элементами орбиты:

| Ключ | Описание |
|------|----------|
| `Semi-major axis` | Большая полуось (км) |
| `Eccentricity` | Эксцентриситет |
| `Inclination` | Наклонение (град) |
| `Semilatus rectum` | Фокальный параметр (км) |
| `RAAN` | Долгота восходящего узла Ω (град) |
| `Argument of perigee` | Аргумент перигея ω (град) |
| `True anomaly` | Истинная аномалия ν (град) |
| `Argument of latitude` | Аргумент широты u (град) |
| `Time since periapsis passage` | Время прохождения перигея `t_p` (datetime) |
| `Eccentric anomaly` | Эксцентрическая аномалия E (град), для эллиптических орбит |
| `Hyperbolic anomaly` | Гиперболическая аномалия H (град), для гиперболических орбит |
| `Mean anomaly` | Средняя аномалия M (град) |
| `Mean motion` | Среднее движение n (рад/с) |
| `Specific orbital energy` | Удельная орбитальная энергия h (км²/с²) |
| `Time difference` | Время от перигея до `t0` (с) |
| `Start time` | Начальное время (datetime) |
| `Start position` | Начальный радиус-вектор (numpy.array) |

**Определяемый тип орбиты:**
- `h < 0` — эллиптическая,
- `h == 0` — параболическая,
- `h > 0` — гиперболическая.

---

### `spacecraft_position_velocity(...)`

Определяет положение и скорость КА в заданный момент времени.

**Сигнатура:**

```python
spacecraft_position_velocity(new_time=5*3600,
                             dict_orbital_elements={},
                             printable=False,
                             main=True)
```

**Параметры:**
- `new_time` — смещение от начального времени в секундах;
- `dict_orbital_elements` — словарь, полученный из `orbital_elements()`;
- `printable` — если `True`, выводит результаты;
- `main` — если `True`, решает уравнение Кеплера итерационно методом простой итерации; иначе берёт эксцентрическую аномалию из словаря.

**Возвращает:** кортеж `(r_vector, V_vector, E_deg)`:
- `r_vector` — радиус-вектор в геоцентрической экваториальной системе (км);
- `V_vector` — вектор скорости (км/с);
- `E_deg` — эксцентрическая аномалия (град).

**Ограничения:**
- Параболические и гиперболические орбиты пока не реализованы; функция выводит сообщение и возвращает `None`.

---

### `construct_motion_trajectory(...)`

Строит трассу движения КА (проекцию орбиты на поверхность Земли) и визуализирует её на карте мира в цилиндрической проекции.

**Сигнатура:**

```python
construct_motion_trajectory(orbital_elements={}, k=2, printable=False)
```

**Параметры:**
- `orbital_elements` — словарь из `orbital_elements()`;
- `k` — количество витков для отображения (по умолчанию `2`);
- `printable` — если `True`, выводит точки трассы `[E°, λ°, φ°]` в консоль.

**Особенности:**
- Трасса строится с шагом 1° по эксцентрической аномалии;
- Долгота корректируется на вращение Земли (`omega_earth`);
- Учитывается разрыв трассы при переходе через меридиан ±180°;
- Начальная точка отмечается красным маркером; начало трассы соответствует `l0 = -94.65°`;
- Используется картографическая подложка (`cartopy`) с сушей, океаном, береговыми линиями и границами.

---

## Пример использования

```python
import orbital_math as orb

# 1. Вычисление элементов орбиты
elements = orb.orbital_elements(printable=True)

# 2. Положение и скорость через 5 часов после старта
r, V, E = orb.spacecraft_position_velocity(
    new_time=5*3600,
    dict_orbital_elements=elements,
    printable=True
)

# 3. Построение трассы на 2 витка
orb.construct_motion_trajectory(elements, k=2)
```

---

## Ограничения и замечания

- Реализованы только эллиптические орбиты (`e < 1`);
- Параболические и гиперболические орбиты пока не поддерживаются;
- Функция `spacecraft_position_velocity` решает уравнение Кеплера методом простой итерации; сходимость гарантирована для `e < 1`, но число итераций может быть значительным при `e`, близком к 1;
- Расчёт долготы в трассе использует упрощённую модель: постоянная угловая скорость вращения Земли, без учёта прецессии и нутации;
