h=5.0;
r_hole=4.5/2.0;
r_cylinder=r_hole*2.5;
$fn=360;

difference()
{
    cylinder(h, r_cylinder, r_cylinder, center=true);
    cylinder(h+1, r_hole, r_hole, center=true);
}