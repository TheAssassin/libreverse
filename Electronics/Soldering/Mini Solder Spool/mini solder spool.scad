/* CONFIGURATION */

// inner hole
spool_hole_radius = 9;

// outer dimensions
spool_outer_radius = 18;
spool_height = 24;

// radius of outer edges
spool_edge_radius = 2;

// minimal thickness of wall between groove and inner hole
spool_groove_wall_thickness = 1;
// cylinder height between groove and edge radius (added both above and below groove)
spool_groove_distance_outer_radius = 1;

/* END OF CONFIGURATION */


difference() {
    $fn = 120;

    // spool
    rotate_extrude() {
        // the groove is basically a circular segment
        // the groove shall maintain a minimum wall in the middle, as well as a cylinder between the outer edge radius
        // known: height (h) and chord length (c)
        groove_seg_height = spool_outer_radius - spool_hole_radius - spool_groove_wall_thickness;
        groove_seg_chord_length = spool_height - 2*spool_edge_radius - 2*spool_groove_distance_outer_radius;

        // the formula to calculate the radius is: r = (4h² + c²) / (8h)
        groove_radius = (
            4*groove_seg_height*groove_seg_height +
            groove_seg_chord_length * groove_seg_chord_length
        ) / (8*groove_seg_height);

        echo("groove segment height", groove_seg_height);
        echo("groove segment chord length", groove_seg_chord_length);
        echo("groove radius", groove_radius);
        echo("groove height", groove_seg_height);

        // make sure groove's radius is larger than the groove's segment height
        assert(groove_radius >= groove_seg_height);

        groove_x_offset = spool_hole_radius + spool_groove_wall_thickness + groove_radius;
        echo("groove X offset", groove_x_offset);

        difference() {
            hull()
            {
                // inner lower corner
                translate([spool_hole_radius + spool_edge_radius, spool_edge_radius])
                circle(spool_edge_radius);

                // inner upper corner
                translate([spool_hole_radius + spool_edge_radius, spool_height - spool_edge_radius])
                circle(spool_edge_radius);

                // outer upper corner
                translate([spool_outer_radius - spool_edge_radius, spool_height - spool_edge_radius])
                circle(spool_edge_radius);

                // outer lower corner
                translate([spool_outer_radius - spool_edge_radius, spool_edge_radius])
                circle(spool_edge_radius);
            }


            // groove (centered)
            translate([groove_x_offset, spool_height/2]) {
                circle(groove_radius);
            }
        }
    }

    // hole for solder wire
    translate([0, 0, spool_height/2]) {
        rotate([90])
        linear_extrude(spool_outer_radius, $fn=120) {
            circle(1);
        }
    }
}
