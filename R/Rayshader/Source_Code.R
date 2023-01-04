# to unzip the file downloaded from kontur population
install.packages('R.utils')
library(R.utils)
df = R.utils::gunzip("C:/Users/Nicole/Desktop/kontur_population_GB_20220630.gpkg.gz")
uk_data = st_read(df)

options(rgl.useNULL = FALSE)

library(sf)
library(tidyverse)
library(tigris)
library(ggplot2)
library(stars)
library(MetBrewer)
library(colorspace)
library(rayshader)
library(units)
units_options(allow_mixed = TRUE)

=
uk_data = st_read("C:/Users/Nicole/Desktop/kontur_population_GB_20220630.gpkg")
uk_data|>
+   ggplot() +
+   geom_sf()

ratio = st_bbox(uk_data)

bl <- st_point(c(ratio[["xmin"]], ratio[["ymin"]])) |>
  st_sfc(crs = st_crs(uk_data))

br <- st_point(c(ratio[["xmax"]], ratio[["ymin"]])) |>
  st_sfc(crs = st_crs(uk_data))

width = st_distance(bl, br)

tl <- st_point(c(ratio[["xmin"]], ratio[["ymax"]])) |>
  st_sfc(crs = st_crs(uk_data))

height <- st_distance(bl, tl)

if(width > height) {
  w_ratio <- 1
  h_ratio <- height / width
} else {
  h_ratio <- 1
  w_ratio <- width / height
}

size <- 5000

a = floor(size * w_ratio)
b = floor(size * h_ratio)

a = as.numeric(a)
b = as.numeric(b)

uk_rast <- st_rasterize(uk_data, nx = a, ny = b)

mp <- mprix(uk_rast$population, nrow = a, ncol = b)

# Create color palette
color <- MetBrewer::met.brewer(name="Cassatt2")

tx <- grDevices::colorRampPalette(color, bias = 1.5)(256)

swatchplot(tx)
swatchplot(color)

library(rgl)
rgl.open()

mp |>
  height_shade(texture = tx) |>
  add_overlay(sphere_shade(mp, texture = "desert",
  zscale= 0.5, colorintensity = 4), alphalayer=0.5) |>
  plot_3d(heightmap = mp,
          zscale = 100 / 5 / 2,
          solid = FALSE,
          shadowdepth = 0,
          shadowcolor = color[7],
          shadow_darkness = 2)

render_camera(theta = 200, phi = 30, zoom =.65)

file <- ("C:/Users/Nicole/Desktop/uk_map.png")

{
  start_time <- Sys.time()
  cat(crayon::cyan(start_time), "\n")
  if(!file.exists(file)) {
    png::writePNG(mprix(1), target = file)
  }
 
  render_highquality (
    filename = file,
    interactive = FALSE,
    lightdirection = 350,
    lightaltitude = c(20,80),
    lightcolor = c(color[5], "white"),
    lightintensity = c(800,200),
    samples = 350,
    height = 3000,
    width = 3000
  )
 
  end_time <- Sys.time()
  diff <- end_time - start_time
  cat(crayon::cyan(diff), "\n")
}
