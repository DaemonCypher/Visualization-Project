<script lang="ts">
    import type { Insurance } from "../types";
    import * as d3 from "d3";
    // define the props of the Bar component
    type Props = {
      movies: TMovie[];
      progress?: number;
      width?: number;
      height?: number;
    };
    
  </script>
