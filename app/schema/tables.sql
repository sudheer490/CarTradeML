create database used_cars;
create table all_cars
-- store information of all unique cars in our database
(
    car_id int,     -- uniquely identifies a car                                                                 
    car_make text,  -- Make of the car                                                              
    car_brand text, -- Brand of the car                                                               
    car_year int,   -- Year                                                                
    primary key(car_id)                                                             
);       

create table car_types
(
    car_type_id int,
    car_type text,
    primary key(car_type_id)
);

create table car_details
(
    cd_id int,
    cd_type_id int,
    cd_mileage_miles float,
    cd_car_price float,
    cd_year int,
    cd_make text,
    cd_model text,
    cd_body_style text,
    cd_doors text,
    cd_mpg text,
    cd_engine text,
    cd_transmission text,
    cd_drive_type text,
    cd_fuel text,
    cd_tank_size text,
    cd_bed_style text,
    cd_cab_style text,
    cd_path_ text,
    primary key(cd_id),
    FOREIGN KEY (cd_type_id) REFERENCES car_types (car_type_id)
);

CREATE TABLE car_features
(
    cf_car_id INT,
    cf_android_auto INT,
    cf_apple_carplay INT,
    cf_backup_camera_assist INT,
    cf_bluetooth INT,
    cf_heated_seats INT,
    cf_hill_assist_system INT,
    cf_keyless_entry INT,
    cf_keyless_ignition INT,
    cf_multimedia_telematics INT,
    cf_premium_sound_system INT,
    cf_satellite_radio INT,
    cf_sunroof_moonroof INT,
    cf_leather_seats INT,
    cf_power_seats INT,
    cf_traction_control INT,
    cf_driver_assistance_confidence_pkg INT,
    cf_head_up_display INT,
    cf_lane_departure_warning INT,
    cf_navigation_system INT,
    cf_remote_start INT,
    cf_blind_spot_monitor INT,
    cf_lane_assist INT,
    cf_parking_assist_system INT,
    cf_stability_control INT,
    cf_adaptive_cruise_control INT,
    cf_alloy_wheels INT,
    cf_cooled_seats INT,
    cf_full_self_driving_capability INT,
    cf_third_row_seating INT,
    cf_tow_hitch_package INT,
    cf_rear_seat_entertainment INT,
    PRIMARY KEY (cf_car_id)
);

create table similarity_matrix
(
    cd_id float ,
    si_0 float,
    si_1 float,
    si_2 float,
    si_3 float,
    si_4 float,
    si_5 float,
    si_6 float,
    si_7 float,
    si_8 float,
    si_9 float,
    PRIMARY KEY(cd_id)
);

